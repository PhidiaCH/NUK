# -*- coding: utf-8 -*-
"""執行知識圖譜節點中的程式碼，並以預設的範例輸入取代 input()。"""
import builtins
import contextlib
import io
import warnings


def run_code(code, stdin=None):
    """執行一段 Python 程式碼，回傳 (stdout 文字, 例外或 None)。"""
    feed = list(stdin or [])
    out = io.StringIO()

    def fake_input(prompt=""):
        out.write(str(prompt))
        value = feed.pop(0) if feed else ""
        out.write(value + "\n")
        return value

    real_input = builtins.input
    builtins.input = fake_input
    err = None
    try:
        with contextlib.redirect_stdout(out), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(code, "<kg>", "exec"), {"__name__": "__kg__"})
    except Exception as e:  # noqa: BLE001 — 回報給呼叫端
        err = e
    finally:
        builtins.input = real_input
    return out.getvalue(), err
