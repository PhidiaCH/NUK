#!/usr/bin/env python3
"""
會議錄音與記錄系統 (Meeting Recorder) v2.0
─────────────────────────────────────────────
功能:
  • 多角色錄音與識別  (主席 / 書記 / 演講者 / 與會者)
  • 說話者自動分離    (pyannote.audio)
  • 語音轉文字        (OpenAI Whisper, 支援中英混合)
  • AI 會議記錄生成   (Claude API)
    ─ 議程重建
    ─ 討論摘要
    ─ 決議事項
    ─ 主席行動指示
    ─ 行動事項 (負責人 / 截止日期 / 優先度)
  • 多格式輸出        (Markdown / JSON / PDF)
  • 支援即時錄音或匯入現有音訊

使用方式:
  # 互動式錄音
  python meeting_recorder.py

  # 處理現有音訊
  python meeting_recorder.py --file audio.wav --title "季度會議"

  # 指定模型 / 語言
  python meeting_recorder.py --whisper-model medium --language zh
"""

import os
import sys
import re
import json
import time
import wave
import threading
import datetime
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum

# ── 選用依賴 ──────────────────────────────────────────────────────────────────

def _try_import(module: str, pkg_hint: str = ""):
    try:
        return __import__(module), True
    except ImportError:
        hint = f" (pip install {pkg_hint})" if pkg_hint else ""
        print(f"[WARN] '{module}' 未安裝{hint}，相關功能停用。")
        return None, False

_pyaudio_mod,    PYAUDIO_OK    = _try_import("pyaudio",    "pyaudio")
_whisper_mod,    WHISPER_OK    = _try_import("whisper",    "openai-whisper")
_pyannote_mod,   PYANNOTE_OK   = _try_import("pyannote.audio", "pyannote.audio")
_anthropic_mod,  ANTHROPIC_OK  = _try_import("anthropic",  "anthropic")
_rich_mod,       RICH_OK       = _try_import("rich",       "rich")
_reportlab_mod,  REPORTLAB_OK  = _try_import("reportlab",  "reportlab")

if PYAUDIO_OK:
    import pyaudio  # noqa: F811
if WHISPER_OK:
    import whisper  # noqa: F811
if PYANNOTE_OK:
    from pyannote.audio import Pipeline as PyannotePipeline
if ANTHROPIC_OK:
    import anthropic  # noqa: F811
if RICH_OK:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    _console = Console()
else:
    _console = None

# ── 資料模型 ──────────────────────────────────────────────────────────────────

class MeetingType(Enum):
    DAILY     = "日常會議"
    FORMAL    = "正式會議"
    SEMINAR   = "研討會"
    WORKSHOP  = "工作坊"
    STANDUP   = "站立會議"
    RESEARCH  = "研究討論"


class SpeakerRole(Enum):
    CHAIR       = "主席"
    SECRETARY   = "書記"
    PRESENTER   = "演講者"
    PARTICIPANT = "與會者"
    FACILITATOR = "主持人"
    UNKNOWN     = "未知"


ROLE_COLORS = {
    SpeakerRole.CHAIR:       "bright_red",
    SpeakerRole.SECRETARY:   "bright_blue",
    SpeakerRole.PRESENTER:   "bright_green",
    SpeakerRole.PARTICIPANT: "bright_yellow",
    SpeakerRole.FACILITATOR: "bright_magenta",
    SpeakerRole.UNKNOWN:     "white",
}


@dataclass
class Speaker:
    id:    str
    name:  str
    role:  SpeakerRole
    color: str = "white"


@dataclass
class Utterance:
    speaker_id:  str
    start_time:  float
    end_time:    float
    text:        str
    confidence:  float = 1.0


# ── UI 工具 ───────────────────────────────────────────────────────────────────

def _print(msg: str):
    if RICH_OK:
        _console.print(msg)
    else:
        print(re.sub(r'\[/?[^\]]+\]', '', msg))


def _print_header(title: str):
    if RICH_OK:
        _console.print(Panel(f"[bold]{title}[/bold]", expand=False))
    else:
        sep = "─" * 52
        print(f"\n{sep}\n  {title}\n{sep}")


def _prompt(msg: str, default: str = "") -> str:
    if RICH_OK:
        return Prompt.ask(msg, default=default) or default
    result = input(f"{msg} [{default}]: ").strip()
    return result if result else default


def _prompt_int(msg: str, min_val: int, max_val: int, default: int) -> int:
    while True:
        raw = _prompt(f"{msg} ({min_val}–{max_val})", default=str(default))
        try:
            n = int(raw)
            if min_val <= n <= max_val:
                return n
        except ValueError:
            pass
        _print(f"請輸入 {min_val} 到 {max_val} 的整數。")


def _format_ts(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s   = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _format_duration(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s   = divmod(rem, 60)
    if h:    return f"{h}小時{m}分{s}秒"
    if m:    return f"{m}分{s}秒"
    return f"{s}秒"


# ── 錄音模組 ──────────────────────────────────────────────────────────────────

class AudioRecorder:
    """麥克風錄音，儲存為 16 kHz 單聲道 WAV（Whisper 最佳格式）。"""

    CHUNK    = 1024
    CHANNELS = 1
    RATE     = 16_000

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.frames:      List[bytes] = []
        self.is_recording = False
        self._pa      = None
        self._stream  = None
        self._thread  = None
        self.start_ts: Optional[float] = None
        self.duration: float = 0.0

    def start(self):
        if not PYAUDIO_OK:
            raise RuntimeError("需要 pyaudio 才能錄音。")
        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format           = pyaudio.paInt16,
            channels         = self.CHANNELS,
            rate             = self.RATE,
            input            = True,
            frames_per_buffer= self.CHUNK,
        )
        self.is_recording = True
        self.start_ts     = time.time()
        self._thread      = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while self.is_recording:
            try:
                data = self._stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            except Exception:
                break

    def stop(self) -> Path:
        self.is_recording = False
        if self._thread:
            self._thread.join(timeout=3)
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._pa:
            fmt = self._pa.get_sample_size(pyaudio.paInt16)
            self._pa.terminate()
        else:
            fmt = 2
        self.duration = time.time() - self.start_ts if self.start_ts else 0
        with wave.open(str(self.output_path), "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(fmt)
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
        return self.output_path


# ── 語音轉文字 ────────────────────────────────────────────────────────────────

class Transcriber:
    """Whisper 語音轉文字，支援中文 / 英文 / 自動偵測。"""

    def __init__(self, model_size: str = "base", language: str = "zh"):
        self.model_size = model_size
        self.language   = language
        self._model     = None

    def _load(self):
        if not WHISPER_OK:
            raise RuntimeError("需要 openai-whisper 才能轉錄語音。")
        if not self._model:
            _print(f"  載入 Whisper [{self.model_size}] 模型…")
            self._model = whisper.load_model(self.model_size)

    def transcribe(self, audio_path: Path) -> Dict:
        self._load()
        lang = self.language if self.language != "auto" else None
        return self._model.transcribe(
            str(audio_path),
            language        = lang,
            verbose         = False,
            word_timestamps = True,
        )


# ── 說話者分離 ────────────────────────────────────────────────────────────────

class SpeakerDiarizer:
    """使用 pyannote.audio 3.x 進行說話者分離（需 HuggingFace token）。"""

    def __init__(self, hf_token: Optional[str] = None):
        self.hf_token  = hf_token or os.environ.get("HF_TOKEN", "")
        self._pipeline = None

    def _load(self):
        if not PYANNOTE_OK:
            raise RuntimeError("需要 pyannote.audio 才能進行說話者分離。")
        if not self._pipeline:
            self._pipeline = PyannotePipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token,
            )

    def diarize(self, audio_path: Path) -> List[Dict]:
        """回傳 [{speaker, start, end}, ...] 清單。"""
        self._load()
        dia = self._pipeline(str(audio_path))
        return [
            {"speaker": spk, "start": turn.start, "end": turn.end}
            for turn, _, spk in dia.itertracks(yield_label=True)
        ]

    @staticmethod
    def align(whisper_result: Dict, segments: List[Dict]) -> List[Utterance]:
        """將 Whisper 片段與說話者標籤對齊。"""
        utterances = []
        for seg in whisper_result.get("segments", []):
            mid    = (seg["start"] + seg["end"]) / 2
            speaker = "UNKNOWN"
            for d in segments:
                if d["start"] <= mid <= d["end"]:
                    speaker = d["speaker"]
                    break
            text = seg["text"].strip()
            if text:
                utterances.append(Utterance(
                    speaker_id = speaker,
                    start_time = seg["start"],
                    end_time   = seg["end"],
                    text       = text,
                ))
        return utterances


# ── 角色管理 ──────────────────────────────────────────────────────────────────

class RoleManager:
    """管理說話者身份與角色指派。"""

    def __init__(self):
        self.speakers: Dict[str, Speaker] = {}

    def assign_interactive(self, speaker_ids: List[str]):
        _print_header("角色指派")
        roles = list(SpeakerRole)
        for sid in sorted(set(speaker_ids)):
            _print(f"\n偵測到說話者: [bold]{sid}[/bold]")
            name = _prompt("  姓名", default=sid)
            _print("  角色: " + "  ".join(
                f"[{i+1}] {r.value}" for i, r in enumerate(roles)
            ))
            idx  = _prompt_int("  選擇", 1, len(roles), default=4)
            role = roles[idx - 1]
            self.speakers[sid] = Speaker(
                id=sid, name=name, role=role, color=ROLE_COLORS[role]
            )

    def get(self, sid: str) -> Speaker:
        if sid not in self.speakers:
            self.speakers[sid] = Speaker(
                id=sid, name=sid,
                role=SpeakerRole.UNKNOWN,
                color=ROLE_COLORS[SpeakerRole.UNKNOWN],
            )
        return self.speakers[sid]

    def chair(self) -> Optional[Speaker]:
        return next(
            (s for s in self.speakers.values() if s.role == SpeakerRole.CHAIR),
            None
        )

    def speaking_stats(self, utterances: List[Utterance]) -> Dict[str, float]:
        """計算各說話者的發言秒數。"""
        stats: Dict[str, float] = {}
        for u in utterances:
            dur = u.end_time - u.start_time
            stats[u.speaker_id] = stats.get(u.speaker_id, 0.0) + dur
        return stats


# ── AI 會議記錄 ───────────────────────────────────────────────────────────────

_MINUTES_PROMPT = """\
你是一位專業的會議記錄員，請根據以下逐字稿生成結構化的繁體中文會議記錄。

【會議資訊】
類型: {meeting_type}
日期: {date}
時長: {duration}
與會者: {attendees}

【逐字稿】
{transcript}

【輸出要求】
請嚴格以合法 JSON 回應，結構如下（不要加任何說明文字）：
{{
  "agenda_items": ["議題1", "議題2"],
  "discussion_summary": "300–500 字的整體討論摘要",
  "key_highlights": ["重點1", "重點2", "重點3"],
  "key_decisions": ["決議1", "決議2"],
  "chair_directives": ["主席指示1", "主席指示2"],
  "action_items": [
    {{
      "assignee": "負責人",
      "description": "行動事項",
      "deadline": "截止日期（未提及填 null）",
      "priority": "高|中|低"
    }}
  ],
  "next_meeting": "下次會議資訊（未提及填 null）"
}}

注意：
- 務必特別提取主席的所有行動指示置於 chair_directives
- action_items 要具體、可執行
- 使用繁體中文
"""


class MinutesGenerator:
    """使用 Claude API 生成結構化會議記錄。"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self._client = None

    def _get_client(self):
        if not ANTHROPIC_OK:
            raise RuntimeError("需要 anthropic SDK 才能生成 AI 會議記錄。")
        if not self._client:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def generate(
        self,
        utterances:   List[Utterance],
        speakers:     Dict[str, Speaker],
        meeting_type: str,
        date:         str,
        duration:     str,
    ) -> Dict:
        lines = []
        for u in utterances:
            spk   = speakers.get(u.speaker_id)
            label = f"{spk.name}（{spk.role.value}）" if spk else u.speaker_id
            lines.append(f"[{_format_ts(u.start_time)}] {label}: {u.text}")

        attendees = ", ".join(
            f"{s.name}（{s.role.value}）" for s in speakers.values()
        )
        prompt = _MINUTES_PROMPT.format(
            meeting_type = meeting_type,
            date         = date,
            duration     = duration,
            attendees    = attendees,
            transcript   = "\n".join(lines),
        )

        client = self._get_client()
        resp   = client.messages.create(
            model      = "claude-opus-4-6",
            max_tokens = 4096,
            messages   = [{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text
        # Robustly extract the JSON block
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        _print("[yellow]AI 回應解析失敗，回傳原始文字。[/yellow]")
        return {"raw_response": raw}


# ── 輸出模組 ──────────────────────────────────────────────────────────────────

class Exporter:

    @staticmethod
    def markdown(
        title: str, meeting_type: str, date: str, duration: str,
        speakers: Dict[str, Speaker],
        utterances: List[Utterance],
        minutes: Dict,
        stats: Dict[str, float],
    ) -> str:
        L = []
        add = L.append

        add(f"# {title}")
        add(f"\n| 欄位 | 內容 |")
        add(f"|------|------|")
        add(f"| 類型 | {meeting_type} |")
        add(f"| 日期 | {date} |")
        add(f"| 時長 | {duration} |")
        add(f"| 記錄生成 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} |")

        # Attendees
        add("\n## 與會者\n")
        total_speech = sum(stats.values()) or 1
        for s in speakers.values():
            pct   = stats.get(s.id, 0) / total_speech * 100
            chair = " ★" if s.role == SpeakerRole.CHAIR else ""
            add(f"- **{s.name}**（{s.role.value}）{chair} — 發言佔比 {pct:.1f}%")

        # Agenda
        if minutes.get("agenda_items"):
            add("\n## 議程\n")
            for i, item in enumerate(minutes["agenda_items"], 1):
                add(f"{i}. {item}")

        # Summary
        if minutes.get("discussion_summary"):
            add("\n## 討論摘要\n")
            add(minutes["discussion_summary"])

        # Highlights
        if minutes.get("key_highlights"):
            add("\n## 重點摘要\n")
            for h in minutes["key_highlights"]:
                add(f"- {h}")

        # Decisions
        if minutes.get("key_decisions"):
            add("\n## 決議事項\n")
            for d in minutes["key_decisions"]:
                add(f"- [ ] {d}")

        # Chair directives
        if minutes.get("chair_directives"):
            add("\n## 主席指示 ★\n")
            for d in minutes["chair_directives"]:
                add(f"- **{d}**")

        # Action items
        if minutes.get("action_items"):
            add("\n## 行動事項\n")
            add("| 負責人 | 事項 | 截止日期 | 優先度 | 狀態 |")
            add("|--------|------|----------|--------|------|")
            for a in minutes["action_items"]:
                add(
                    f"| {a.get('assignee','')} "
                    f"| {a.get('description','')} "
                    f"| {a.get('deadline') or '—'} "
                    f"| {a.get('priority','中')} "
                    f"| ☐ 待辦 |"
                )

        # Next meeting
        if minutes.get("next_meeting"):
            add(f"\n## 下次會議\n\n{minutes['next_meeting']}")

        # Full transcript
        add("\n---\n")
        add("## 完整逐字稿\n")
        for u in utterances:
            spk   = speakers.get(u.speaker_id)
            label = f"**{spk.name}**（{spk.role.value}）" if spk else u.speaker_id
            add(f"`{_format_ts(u.start_time)}` {label}: {u.text}\n")

        return "\n".join(L)

    @staticmethod
    def json_dump(
        title: str, meeting_type: str, date: str, duration: str,
        speakers: Dict[str, Speaker],
        utterances: List[Utterance],
        minutes: Dict,
        stats: Dict[str, float],
    ) -> str:
        data = {
            "title":        title,
            "meeting_type": meeting_type,
            "date":         date,
            "duration":     duration,
            "generated_at": datetime.datetime.now().isoformat(),
            "attendees": [
                {
                    "id":             s.id,
                    "name":           s.name,
                    "role":           s.role.value,
                    "speaking_secs":  round(stats.get(s.id, 0), 1),
                }
                for s in speakers.values()
            ],
            "minutes": minutes,
            "transcript": [
                {
                    "speaker_id":   u.speaker_id,
                    "speaker_name": speakers[u.speaker_id].name
                                    if u.speaker_id in speakers else u.speaker_id,
                    "role":         speakers[u.speaker_id].role.value
                                    if u.speaker_id in speakers else "未知",
                    "start":        round(u.start_time, 2),
                    "end":          round(u.end_time, 2),
                    "text":         u.text,
                }
                for u in utterances
            ],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def pdf(
        out_path: Path,
        title: str, meeting_type: str, date: str, duration: str,
        speakers: Dict[str, Speaker],
        utterances: List[Utterance],
        minutes: Dict,
        stats: Dict[str, float],
    ):
        """
        使用 reportlab 輸出 A4 繁體中文 PDF。
        內建 CID CJK 字型 (STSong-Light)，無需外部字型檔。
        """
        if not REPORTLAB_OK:
            raise RuntimeError("需要 reportlab 才能輸出 PDF。(pip install reportlab)")

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer,
            Table, TableStyle, HRFlowable, PageBreak,
        )
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont

        # ── 字型（優先嵌入 TrueType，確保跨平台顯示；降級至 CID）────────────────
        _FONT_CANDIDATES = [
            # Linux (WenQuanYi)
            ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",         0),
            ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",       0),
            # Linux (Noto CJK)
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 1),
            ("/usr/share/fonts/truetype/noto/NotoSansCJKtc-Regular.otf", None),
            # macOS
            ("/System/Library/Fonts/PingFang.ttc",                    0),
            ("/Library/Fonts/Arial Unicode MS.ttf",                   None),
            # Windows
            ("C:/Windows/Fonts/msjh.ttc",                             0),
            ("C:/Windows/Fonts/mingliu.ttc",                          0),
        ]
        _FONT = "CJKEmbedded"
        _font_registered = False
        for _path, _idx in _FONT_CANDIDATES:
            if Path(_path).exists():
                try:
                    kw = {"subfontIndex": _idx} if _idx is not None else {}
                    pdfmetrics.registerFont(TTFont(_FONT, _path, **kw))
                    _font_registered = True
                    break
                except Exception:
                    continue
        if not _font_registered:
            # 降級：使用內建 CID 字型（需 PDF 閱覽器具備 CJK 字型包）
            _FONT = "STSong-Light"
            try:
                pdfmetrics.registerFont(UnicodeCIDFont(_FONT))
            except Exception:
                pass

        # ── 顏色定義 ──────────────────────────────────────────────────────────
        C_NAVY   = colors.HexColor("#1a2642")
        C_BLUE   = colors.HexColor("#2c4a8c")
        C_RED    = colors.HexColor("#c0392b")
        C_REDBG  = colors.HexColor("#fff5f5")
        C_STRIPE = colors.HexColor("#f0f4ff")
        C_STRAW  = colors.HexColor("#fff8f0")
        C_GREY   = colors.HexColor("#666666")
        C_LGREY  = colors.HexColor("#cccccc")
        C_LINE   = colors.HexColor("#dddddd")
        C_ROWBG  = colors.HexColor("#f8f8f8")

        # ── 段落樣式工廠 ──────────────────────────────────────────────────────
        def _ps(name, size=10, before=0, after=4, leading=None, color=colors.black,
                indent=0, bold=False):
            return ParagraphStyle(
                name,
                fontName  = _FONT,
                fontSize  = size,
                spaceBefore = before,
                spaceAfter  = after,
                leading     = leading or size * 1.6,
                textColor   = color,
                leftIndent  = indent,
                wordWrap    = "CJK",
            )

        S_TITLE  = _ps("Title",  size=20, after=6,  color=C_NAVY)
        S_H1     = _ps("H1",     size=13, before=14, after=4, color=C_NAVY)
        S_BODY   = _ps("Body",   size=10, after=4)
        S_BULLET = _ps("Bullet", size=10, after=3,  indent=12)
        S_CHAIR  = _ps("Chair",  size=10, after=0,  color=C_RED, indent=6)
        S_META   = _ps("Meta",   size=8,  after=1,  color=C_GREY)
        S_TS_TXT = _ps("TsTxt",  size=9,  after=4)

        # ── 文件設定 ──────────────────────────────────────────────────────────
        PAGE_W, PAGE_H = A4
        MARGIN = 2.5 * cm
        BODY_W = PAGE_W - 2 * MARGIN   # ~16 cm

        doc = SimpleDocTemplate(
            str(out_path),
            pagesize     = A4,
            leftMargin   = MARGIN,
            rightMargin  = MARGIN,
            topMargin    = MARGIN,
            bottomMargin = MARGIN,
            title        = title,
            author       = "Meeting Recorder v2.0",
        )

        elems = []

        def _hr(thick=0.5, color=C_LGREY, after=8):
            elems.append(HRFlowable(
                width=f"100%", thickness=thick, color=color, spaceAfter=after
            ))

        def _section(text):
            elems.append(Spacer(1, 6))
            elems.append(Paragraph(text, S_H1))
            _hr(thick=1.2, color=C_BLUE, after=6)

        def _tbl_style(header_color=C_NAVY, stripe=C_STRIPE, has_header=True):
            cmds = [
                ("FONTNAME",  (0, 0), (-1, -1), _FONT),
                ("FONTSIZE",  (0, 0), (-1, -1), 9),
                ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING",   (0, 0), (-1, -1), 5),
                ("GRID",      (0, 0), (-1, -1), 0.3, C_LINE),
                ("WORDWRAP",  (0, 0), (-1, -1), "CJK"),
            ]
            if has_header:
                cmds += [
                    ("BACKGROUND", (0, 0), (-1, 0), header_color),
                    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE",   (0, 0), (-1, 0), 9),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.white, stripe]),
                ]
            else:
                cmds += [
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1),
                     [C_ROWBG, colors.white]),
                    ("TEXTCOLOR", (0, 0), (0, -1), C_GREY),
                ]
            return TableStyle(cmds)

        # ── 標題區 ────────────────────────────────────────────────────────────
        elems.append(Paragraph(title, S_TITLE))
        _hr(thick=2, color=C_NAVY, after=10)

        # 會議資訊表
        info_rows = [
            ["類型", meeting_type],
            ["日期", date],
            ["時長", duration],
            ["記錄生成", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
        ]
        info_tbl = Table(info_rows, colWidths=[3 * cm, BODY_W - 3 * cm])
        info_tbl.setStyle(_tbl_style(has_header=False))
        elems.append(info_tbl)

        # ── 與會者 ────────────────────────────────────────────────────────────
        _section("與會者")
        total_speech = sum(stats.values()) or 1
        att_rows = [["姓名", "角色", "發言時長", "佔比"]]
        for s in speakers.values():
            dur = stats.get(s.id, 0)
            pct = dur / total_speech * 100
            star = " ★" if s.role == SpeakerRole.CHAIR else ""
            att_rows.append([
                Paragraph(f"{s.name}{star}", S_BODY),
                Paragraph(s.role.value, S_BODY),
                Paragraph(_format_duration(dur), S_BODY),
                Paragraph(f"{pct:.1f}%", S_BODY),
            ])
        att_tbl = Table(
            att_rows,
            colWidths=[4 * cm, 3.5 * cm, 3.5 * cm, 2 * cm],
        )
        att_tbl.setStyle(_tbl_style())
        elems.append(att_tbl)

        # ── 議程 ──────────────────────────────────────────────────────────────
        if minutes.get("agenda_items"):
            _section("議程")
            for i, item in enumerate(minutes["agenda_items"], 1):
                elems.append(Paragraph(f"{i}.  {item}", S_BULLET))

        # ── 討論摘要 ──────────────────────────────────────────────────────────
        if minutes.get("discussion_summary"):
            _section("討論摘要")
            elems.append(Paragraph(minutes["discussion_summary"], S_BODY))

        # ── 重點摘要 ──────────────────────────────────────────────────────────
        if minutes.get("key_highlights"):
            _section("重點摘要")
            for h in minutes["key_highlights"]:
                elems.append(Paragraph(f"▶  {h}", S_BULLET))

        # ── 決議事項 ──────────────────────────────────────────────────────────
        if minutes.get("key_decisions"):
            _section("決議事項")
            for d in minutes["key_decisions"]:
                elems.append(Paragraph(f"[ ]  {d}", S_BULLET))

        # ── 主席指示（紅框高亮） ─────────────────────────────────────────────
        if minutes.get("chair_directives"):
            _section("主席指示 ★")
            for d in minutes["chair_directives"]:
                inner = Table(
                    [[Paragraph(f"▸  {d}", S_CHAIR)]],
                    colWidths=[BODY_W],
                )
                inner.setStyle(TableStyle([
                    ("FONTNAME",      (0, 0), (-1, -1), _FONT),
                    ("BACKGROUND",    (0, 0), (-1, -1), C_REDBG),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
                    ("TOPPADDING",    (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("BOX",           (0, 0), (-1, -1), 1.5, C_RED),
                ]))
                elems.append(inner)
                elems.append(Spacer(1, 5))

        # ── 行動事項表 ────────────────────────────────────────────────────────
        if minutes.get("action_items"):
            _section("行動事項")
            # 使用 Paragraph 確保長文字在儲存格內自動換行
            _cell = lambda t: Paragraph(str(t), S_BODY)
            ai_rows = [["負責人", "行動事項", "截止日期", "優先度", "狀態"]]
            for a in minutes["action_items"]:
                ai_rows.append([
                    _cell(a.get("assignee", "")),
                    _cell(a.get("description", "")),
                    _cell(a.get("deadline") or "—"),
                    _cell(a.get("priority", "中")),
                    _cell("待辦"),
                ])
            ai_tbl = Table(
                ai_rows,
                colWidths=[2.5 * cm, 5.0 * cm, 4.2 * cm, 1.8 * cm, 1.5 * cm],
                repeatRows=1,
            )
            ai_tbl.setStyle(_tbl_style(stripe=C_STRAW))
            elems.append(ai_tbl)

        # ── 下次會議 ──────────────────────────────────────────────────────────
        if minutes.get("next_meeting"):
            _section("下次會議")
            elems.append(Paragraph(minutes["next_meeting"], S_BODY))

        # ── 完整逐字稿（新頁） ────────────────────────────────────────────────
        elems.append(PageBreak())
        elems.append(Paragraph("完整逐字稿", S_H1))
        _hr(thick=1.2, color=C_BLUE, after=8)

        for u in utterances:
            spk   = speakers.get(u.speaker_id)
            label = f"{spk.name}（{spk.role.value}）" if spk else u.speaker_id
            elems.append(Paragraph(
                f"[{_format_ts(u.start_time)}]  {label}", S_META
            ))
            elems.append(Paragraph(u.text, S_TS_TXT))

        doc.build(elems)


# ── 終端摘要顯示 ───────────────────────────────────────────────────────────────

def _display_summary(minutes: Dict, speakers: Dict[str, Speaker], stats: Dict[str, float]):
    if not RICH_OK:
        return

    total = sum(stats.values()) or 1

    # Speaking time table
    spk_table = Table(title="發言時間統計", show_lines=True)
    spk_table.add_column("姓名",   style="bold")
    spk_table.add_column("角色",   style="dim")
    spk_table.add_column("時長",   justify="right")
    spk_table.add_column("佔比",   justify="right")
    for s in speakers.values():
        dur = stats.get(s.id, 0)
        pct = dur / total * 100
        spk_table.add_row(
            s.name, s.role.value,
            _format_duration(dur), f"{pct:.1f}%",
            style=s.color,
        )
    _console.print("\n", spk_table)

    # Highlights
    if minutes.get("key_highlights"):
        _console.print("\n[bold cyan]重點摘要[/bold cyan]")
        for h in minutes["key_highlights"]:
            _console.print(f"  [cyan]•[/cyan] {h}")

    # Chair directives
    if minutes.get("chair_directives"):
        _console.print("\n[bold bright_red]主席指示 ★[/bold bright_red]")
        for d in minutes["chair_directives"]:
            _console.print(f"  [bright_red]▸[/bright_red] {d}")

    # Action items
    if minutes.get("action_items"):
        ai_table = Table(title="行動事項", show_lines=True)
        ai_table.add_column("負責人", style="bold")
        ai_table.add_column("事項")
        ai_table.add_column("截止日期", justify="center")
        ai_table.add_column("優先度",   justify="center")
        PCOLORS = {"高": "bright_red", "中": "yellow", "低": "bright_green"}
        for a in minutes["action_items"]:
            pri = a.get("priority", "中")
            ai_table.add_row(
                a.get("assignee",    ""),
                a.get("description", ""),
                a.get("deadline")  or "—",
                f"[{PCOLORS.get(pri,'white')}]{pri}[/{PCOLORS.get(pri,'white')}]",
            )
        _console.print("\n", ai_table)


# ── 主協調類別 ────────────────────────────────────────────────────────────────

class MeetingRecorder:

    def __init__(self, cfg: Dict):
        self.cfg        = cfg
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.out_dir    = Path(cfg.get("output_dir", "meetings")) / self.session_id
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.role_mgr    = RoleManager()
        self.transcriber = Transcriber(
            model_size = cfg.get("whisper_model", "base"),
            language   = cfg.get("language", "zh"),
        )
        self.diarizer  = SpeakerDiarizer(hf_token=cfg.get("hf_token"))
        self.gen       = MinutesGenerator(api_key=cfg.get("anthropic_api_key"))

        self.utterances: List[Utterance]   = []
        self.audio_path: Optional[Path]    = None
        self.t0: Optional[datetime.datetime] = None
        self.t1: Optional[datetime.datetime] = None

    # ── 互動式設定 ─────────────────────────────────────────────────────────────

    def _setup_interactive(self) -> Tuple[str, str]:
        _print_header("會議錄音與記錄系統 v2.0")
        types = list(MeetingType)
        _print("\n[bold]會議類型:[/bold]")
        for i, t in enumerate(types, 1):
            _print(f"  [{i}] {t.value}")
        idx  = _prompt_int("選擇類型", 1, len(types), default=1)
        mtype = types[idx - 1].value

        default_title = f"{mtype} — {datetime.date.today().strftime('%Y/%m/%d')}"
        title = _prompt("會議標題", default=default_title)
        return title, mtype

    # ── 錄音 ───────────────────────────────────────────────────────────────────

    def _record(self) -> Path:
        audio_path = self.out_dir / "audio.wav"
        recorder   = AudioRecorder(audio_path)

        _print("\n[bold green]▶  開始錄音[/bold green] — 按 [bold]Enter[/bold] 停止錄音")
        self.t0 = datetime.datetime.now()
        recorder.start()
        try:
            input()
        except KeyboardInterrupt:
            pass
        _print("[bold yellow]■  停止錄音…[/bold yellow]")
        recorder.stop()
        self.t1 = datetime.datetime.now()
        self.audio_path = audio_path
        _print(f"錄音完成，時長 [bold]{_format_duration(recorder.duration)}[/bold]")
        return audio_path

    # ── 音訊處理 ───────────────────────────────────────────────────────────────

    def _process(self, audio_path: Path) -> List[Utterance]:
        _print("\n[bold]正在處理音訊…[/bold]")

        # 說話者分離
        dia_segs: List[Dict] = []
        if PYANNOTE_OK and self.cfg.get("hf_token"):
            _print("  說話者分離中…")
            try:
                dia_segs = self.diarizer.diarize(audio_path)
                n_spk = len(set(d["speaker"] for d in dia_segs))
                _print(f"  [green]偵測到 {n_spk} 位說話者[/green]")
            except Exception as e:
                _print(f"  [yellow]說話者分離失敗: {e}[/yellow]")
        else:
            _print("  [dim]說話者分離已跳過（需 HF_TOKEN）[/dim]")

        # 語音轉文字
        _print("  語音轉文字中…")
        w_result = self.transcriber.transcribe(audio_path)

        # 合併
        if dia_segs:
            utterances = SpeakerDiarizer.align(w_result, dia_segs)
        else:
            utterances = [
                Utterance(
                    speaker_id = "SPEAKER_00",
                    start_time = seg["start"],
                    end_time   = seg["end"],
                    text       = seg["text"].strip(),
                )
                for seg in w_result.get("segments", [])
                if seg["text"].strip()
            ]

        _print(f"  [green]共 {len(utterances)} 段語音片段[/green]")

        # 角色指派
        speaker_ids = list(set(u.speaker_id for u in utterances))
        self.role_mgr.assign_interactive(speaker_ids)
        self.utterances = utterances
        return utterances

    # ── AI 會議記錄 ────────────────────────────────────────────────────────────

    def _generate_minutes(self, title: str, mtype: str) -> Dict:
        if not ANTHROPIC_OK or not self.cfg.get("anthropic_api_key"):
            _print("[dim]AI 會議記錄已跳過（需 ANTHROPIC_API_KEY）[/dim]")
            return {}
        _print("\n[bold]正在生成 AI 會議記錄…[/bold]")
        duration = _format_duration(
            (self.t1 - self.t0).total_seconds() if self.t0 and self.t1 else 0
        )
        try:
            return self.gen.generate(
                utterances   = self.utterances,
                speakers     = self.role_mgr.speakers,
                meeting_type = mtype,
                date         = self.t0.strftime("%Y-%m-%d %H:%M") if self.t0 else "",
                duration     = duration,
            )
        except Exception as e:
            _print(f"[yellow]AI 生成失敗: {e}[/yellow]")
            return {}

    # ── 輸出 ───────────────────────────────────────────────────────────────────

    def _export(self, title: str, mtype: str, minutes: Dict):
        duration = _format_duration(
            (self.t1 - self.t0).total_seconds() if self.t0 and self.t1 else 0
        )
        date_str = self.t0.strftime("%Y-%m-%d %H:%M") if self.t0 else ""
        stats    = self.role_mgr.speaking_stats(self.utterances)

        md_path   = self.out_dir / "minutes.md"
        json_path = self.out_dir / "data.json"
        pdf_path  = self.out_dir / "minutes.pdf"

        common_args = (
            title, mtype, date_str, duration,
            self.role_mgr.speakers, self.utterances, minutes, stats,
        )

        md_path.write_text(
            Exporter.markdown(*common_args),
            encoding="utf-8",
        )
        json_path.write_text(
            Exporter.json_dump(*common_args),
            encoding="utf-8",
        )

        pdf_ok = False
        if REPORTLAB_OK:
            try:
                Exporter.pdf(pdf_path, *common_args)
                pdf_ok = True
            except Exception as e:
                _print(f"[yellow]PDF 輸出失敗: {e}[/yellow]")

        _print(f"\n[bold green]✓ 輸出完成[/bold green]")
        _print(f"  📄 Markdown : {md_path}")
        _print(f"  📦 JSON     : {json_path}")
        if pdf_ok:
            _print(f"  📑 PDF      : {pdf_path}")

        if minutes:
            _display_summary(minutes, self.role_mgr.speakers, stats)

    # ── 公開入口 ───────────────────────────────────────────────────────────────

    def run(self):
        """互動式完整流程：設定 → 錄音 → 處理 → 生成 → 輸出。"""
        title, mtype = self._setup_interactive()
        audio_path   = self._record()
        self._process(audio_path)
        minutes      = self._generate_minutes(title, mtype)
        self._export(title, mtype, minutes)

    def run_file(self, audio_path: Path, title: str, mtype: str):
        """處理現有音訊檔案。"""
        if not audio_path.exists():
            _print(f"[red]錯誤: 找不到檔案 {audio_path}[/red]")
            sys.exit(1)
        self.audio_path = audio_path
        self.t0 = datetime.datetime.now()
        self._process(audio_path)
        self.t1 = datetime.datetime.now()
        minutes = self._generate_minutes(title, mtype)
        self._export(title, mtype, minutes)


# ── CLI 入口 ──────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="會議錄音與記錄系統 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
環境變數:
  ANTHROPIC_API_KEY   Anthropic API 金鑰（AI 會議記錄）
  HF_TOKEN            HuggingFace token（說話者分離）

範例:
  # 互動式錄音
  python meeting_recorder.py

  # 處理現有音訊
  python meeting_recorder.py -f recording.wav -t "Q2 專案會議" --type 正式會議

  # 使用較大模型提高精度
  python meeting_recorder.py --whisper-model medium --language auto
        """,
    )
    p.add_argument("--file",  "-f", help="現有音訊檔案路徑（WAV 格式）")
    p.add_argument("--title", "-t", help="會議標題")
    p.add_argument("--type",        help="會議類型（如: 正式會議、研討會）")
    p.add_argument(
        "--whisper-model", default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper 模型大小（精度 vs 速度）[預設: base]",
    )
    p.add_argument(
        "--language", default="zh",
        help="語音語言代碼，如 zh / en / auto [預設: zh]",
    )
    p.add_argument("--output-dir", default="meetings", help="輸出根目錄 [預設: meetings]")
    p.add_argument("--hf-token",   help="HuggingFace token（覆蓋 HF_TOKEN）")
    p.add_argument("--api-key",    help="Anthropic API key（覆蓋 ANTHROPIC_API_KEY）")
    return p


def main():
    args = _build_parser().parse_args()

    cfg = {
        "whisper_model":    args.whisper_model,
        "language":         args.language,
        "output_dir":       args.output_dir,
        "hf_token":         args.hf_token or os.environ.get("HF_TOKEN", ""),
        "anthropic_api_key": args.api_key or os.environ.get("ANTHROPIC_API_KEY", ""),
    }

    recorder = MeetingRecorder(cfg)

    if args.file:
        title = args.title or Path(args.file).stem
        mtype = args.type  or MeetingType.FORMAL.value
        recorder.run_file(Path(args.file), title, mtype)
    else:
        recorder.run()


if __name__ == "__main__":
    main()
