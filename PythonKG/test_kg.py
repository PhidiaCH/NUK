# -*- coding: utf-8 -*-
"""驗證知識圖譜結構與所有程式碼可正確執行。  執行：python -m pytest test_kg.py"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from kg_data import build_graph  # noqa: E402
from runner import run_code  # noqa: E402

G = build_graph()
NODES = {n["id"]: n for n in G["nodes"]}
PY = [n for n in G["nodes"] if n["code"] and n["lang"] == "python"]


def test_every_node_reachable_from_root():
    children = {}
    for e in G["edges"]:
        if e["rel"] == "contains":
            children.setdefault(e["source"], []).append(e["target"])
    seen, stack = set(), ["root"]
    while stack:
        cur = stack.pop()
        if cur not in seen:
            seen.add(cur)
            stack.extend(children.get(cur, []))
    assert seen == set(NODES), set(NODES) - seen


def test_each_node_has_one_parent():
    parents = {}
    for e in G["edges"]:
        if e["rel"] == "contains":
            parents.setdefault(e["target"], []).append(e["source"])
    multi = {k: v for k, v in parents.items() if len(v) > 1}
    assert not multi


@pytest.mark.parametrize("n", PY, ids=[n["id"] for n in PY])
def test_code_runs(n):
    out, err = run_code(n["code"], n["stdin"])
    assert err is None, f"{n['id']}: {err!r}\n{out}"


def _out(id):
    out, err = run_code(NODES[id]["code"], NODES[id]["stdin"])
    assert err is None
    return out


def test_gcd():
    assert "GCD =  3" in _out("ex_gcd")


def test_golden_ratio_without_decimal():
    assert "1.618033988749894848204586834365" in _out("q2_golden_int")


def test_cube_root():
    out = _out("q3_5")
    assert "cbrt(-8) = -2.000" in out
    assert "cbrt(2) = 1.25992104989487316476721060727822835057025146470150" in out


def test_coprime_count():
    assert "個數 = 533" in _out("q3_4")


def test_word_count_matches_lecture_hint():
    out = _out("q5_5").splitlines()
    table = {line.split()[0]: int(line.split()[1]) for line in out if line.strip()}
    assert table["'Cause"] == 1 and table["All"] == 2 and table["For"] == 5
    assert table["with"] == 2 and table["you"] == 3 and table["world"] == 1
    assert out[0].startswith("'Cause") and out[-1].startswith("you")


def test_exercise_4_1():
    expected = ("['Fly', 'robin', 'fly', 'Fly', 'robin', 'fly', 'Fly', 'robin', "
                "'fly', 'Up', 'up', 'to', 'the', 'sky']")
    assert _out("q4_1").splitlines()[0] == expected


def test_queue_is_fifo():
    out = _out("q4_2")
    assert out.index("dequeue :  a") < out.index("dequeue :  b") < out.index("dequeue :  c")
