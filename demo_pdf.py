#!/usr/bin/env python3
"""產生示範會議記錄 PDF。"""

import sys
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from meeting_recorder import (
    Exporter, Speaker, SpeakerRole, Utterance
)

# ── 示範資料 ──────────────────────────────────────────────────────────────────

SPEAKERS = {
    "SPEAKER_00": Speaker(id="SPEAKER_00", name="陳志遠", role=SpeakerRole.CHAIR,       color="bright_red"),
    "SPEAKER_01": Speaker(id="SPEAKER_01", name="林雅婷", role=SpeakerRole.SECRETARY,   color="bright_blue"),
    "SPEAKER_02": Speaker(id="SPEAKER_02", name="王建宏", role=SpeakerRole.PRESENTER,   color="bright_green"),
    "SPEAKER_03": Speaker(id="SPEAKER_03", name="張怡君", role=SpeakerRole.PARTICIPANT, color="bright_yellow"),
}

UTTERANCES = [
    Utterance("SPEAKER_00",  0.0,   8.5,  "本次會議正式開始，請各位確認議程，今天主要討論 Q2 產品路線圖與資源分配問題。"),
    Utterance("SPEAKER_01",  9.0,  14.0,  "已確認出席名單，今日共四人出席，議程如預定。"),
    Utterance("SPEAKER_02", 15.0,  45.0,  "根據 Q1 數據分析，用戶留存率提升了 12%，主要歸因於新手引導流程的優化。Q2 我們計畫推出三個核心功能：智慧推薦引擎、多語言支援，以及效能監控儀表板。"),
    Utterance("SPEAKER_03", 46.0,  60.0,  "關於智慧推薦引擎，目前工程端的估算是六週開發週期，需要兩位後端工程師和一位資料科學家。"),
    Utterance("SPEAKER_00", 61.0,  75.0,  "資源配置方面，我指示建宏在本週五前提交詳細的人力需求報告，並評估是否需要外部顧問協助資料模型設計。"),
    Utterance("SPEAKER_02", 76.0,  90.0,  "收到，我會在週五前完成報告，同時也會列出三家潛在的外部顧問廠商供參考。"),
    Utterance("SPEAKER_03", 91.0, 108.0,  "多語言支援部分，建議優先做繁體中文和英文，日文可以排到 Q3，這樣可以集中資源在最大用戶群。"),
    Utterance("SPEAKER_00",109.0, 125.0,  "同意怡君的建議。另外，我要求林雅婷在下週二前整理競品多語言支援的分析報告，作為我們決策的參考依據。"),
    Utterance("SPEAKER_01",126.0, 132.0,  "好的，我會在週二前完成競品分析。"),
    Utterance("SPEAKER_02",133.0, 155.0,  "效能監控儀表板是相對獨立的功能，我們已有現成的開源方案可以整合，估計兩週內可以完成初版。這個功能對於 SRE 團隊日常運維很有幫助。"),
    Utterance("SPEAKER_00",156.0, 175.0,  "很好。那我們決議 Q2 功能優先順序為：第一智慧推薦、第二效能儀表板、第三多語言（繁中英）。所有功能需在六月底前完成 Beta 測試。"),
    Utterance("SPEAKER_03",176.0, 188.0,  "關於測試資源，能否請行銷部門協助招募 Beta 測試用戶？預計需要 50 到 100 位活躍用戶。"),
    Utterance("SPEAKER_00",189.0, 205.0,  "我來協調行銷部門，目標在五月底前確認 Beta 用戶名單。怡君，請你負責起草用戶測試計畫書，兩週內交給我審閱。"),
    Utterance("SPEAKER_03",206.0, 210.0,  "沒問題，兩週內完成。"),
    Utterance("SPEAKER_01",211.0, 218.0,  "下次會議建議排在四月二十三日，進行 Q2 開發進度中期檢討。"),
    Utterance("SPEAKER_00",219.0, 228.0,  "確認，下次會議四月二十三日上午十點，線上進行。請各位提前準備進度報告。會議到此結束，謝謝大家。"),
]

MINUTES = {
    "agenda_items": [
        "Q1 成果回顧與 Q2 目標確認",
        "Q2 產品路線圖討論：智慧推薦引擎、多語言支援、效能儀表板",
        "資源分配與人力規劃",
        "Beta 測試策略",
    ],
    "discussion_summary": (
        "本次會議由陳志遠主席主持，針對 Q2 產品路線圖進行深入討論。"
        "王建宏報告 Q1 成果，用戶留存率提升 12%，新手引導優化為主要貢獻因素。"
        "Q2 計畫三大核心功能：智慧推薦引擎（6 週，需後端+資料科學家資源）、"
        "效能監控儀表板（2 週，可整合開源方案）、多語言支援（繁中英優先，日文移至 Q3）。"
        "資源配置方面，討論是否引入外部顧問協助資料模型設計。"
        "Beta 測試計畫決議委由行銷部門招募 50–100 位活躍用戶，預計五月底完成名單確認。"
    ),
    "key_highlights": [
        "Q1 用戶留存率提升 12%，新手引導優化效果顯著",
        "Q2 三大功能優先順序：智慧推薦 > 效能儀表板 > 多語言（繁中英）",
        "日文支援延至 Q3，集中資源於主要用戶群",
        "所有功能目標六月底前完成 Beta 測試",
        "需評估外部顧問協助資料模型設計可行性",
    ],
    "key_decisions": [
        "Q2 功能優先順序確認：智慧推薦引擎 > 效能監控儀表板 > 多語言（繁中英）",
        "多語言支援 Q2 僅做繁體中文與英文，日文排入 Q3",
        "所有 Q2 功能須於六月底前完成 Beta 測試",
        "Beta 測試招募目標 50–100 位活躍用戶",
    ],
    "chair_directives": [
        "【王建宏】本週五前提交詳細人力需求報告，並評估外部顧問廠商（列三家以上）",
        "【林雅婷】下週二前完成競品多語言支援分析報告",
        "【張怡君】兩週內完成用戶測試計畫書並交主席審閱",
        "【主席】協調行銷部門，五月底前確認 Beta 用戶名單（50–100 人）",
    ],
    "action_items": [
        {"assignee": "王建宏", "description": "提交 Q2 人力需求報告並列潛在外部顧問廠商", "deadline": "2026-04-11（週五）", "priority": "高"},
        {"assignee": "林雅婷", "description": "完成競品多語言支援分析報告",              "deadline": "2026-04-15（週二）", "priority": "高"},
        {"assignee": "張怡君", "description": "撰寫 Beta 用戶測試計畫書供主席審閱",        "deadline": "2026-04-23",        "priority": "中"},
        {"assignee": "陳志遠", "description": "協調行銷部門招募 50–100 位 Beta 測試用戶",  "deadline": "2026-05-31",        "priority": "中"},
        {"assignee": "王建宏", "description": "效能監控儀表板初版開發完成",               "deadline": "2026-04-23",        "priority": "低"},
    ],
    "next_meeting": "2026 年 4 月 23 日（週四）上午 10:00，線上會議 — Q2 開發進度中期檢討",
}

STATS = {
    "SPEAKER_00": 61.5,
    "SPEAKER_01": 19.0,
    "SPEAKER_02": 57.0,
    "SPEAKER_03": 30.0,
}

# ── 輸出 PDF ──────────────────────────────────────────────────────────────────

out = Path("/home/user/NUK/demo_meeting_minutes.pdf")

Exporter.pdf(
    out_path     = out,
    title        = "Q2 產品路線圖規劃會議",
    meeting_type = "正式會議",
    date         = "2026-04-09 10:00",
    duration     = "3分48秒",
    speakers     = SPEAKERS,
    utterances   = UTTERANCES,
    minutes      = MINUTES,
    stats        = STATS,
)

print(f"PDF 已產生：{out}")
