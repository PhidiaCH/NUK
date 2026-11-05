# -*- coding: utf-8 -*-
"""
Python 知識圖譜 命令列查詢工具

  python kg.py search 切片            # 關鍵字搜尋 (標題、說明、標籤、程式碼)
  python kg.py show c_slicing          # 顯示知識點、程式碼與所有關係
  python kg.py code ex_gcd             # 只輸出程式碼 (可導向存檔: > gcd.py)
  python kg.py run ex_gcd              # 直接執行該段程式
  python kg.py tree [ch3]              # 章節樹狀結構
  python kg.py path ex_fib q5_5        # 找出兩個知識點之間的關聯路徑
  python kg.py list exercise [3]       # 依類型 (與章節) 列出知識點
  python kg.py stats                   # 統計
"""
import argparse
import collections
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kg_data import build_graph  # noqa: E402

G = build_graph()
NODES = {n["id"]: n for n in G["nodes"]}
KINDS = G["meta"]["kinds"]
OUT, INC = collections.defaultdict(list), collections.defaultdict(list)
for e in G["edges"]:
    OUT[e["source"]].append(e)
    INC[e["target"]].append(e)
REL_TEXT = {
    "contains": ("包含", "屬於"), "uses": ("使用到", "被使用於"),
    "related": ("相關", "相關"), "refactors": ("改寫自", "被改寫為"),
    "practice": ("練習對象", "練習題"), "prereq": ("之後學習", "前置知識"),
}


def _fix_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def tag(n):
    return f"[{KINDS[n['kind']]}] {n['label']}  ({n['id']})"


def resolve(key):
    if key in NODES:
        return NODES[key]
    hits = search(key)
    if not hits:
        sys.exit(f"找不到知識點：{key}")
    if len(hits) > 1:
        print(f"「{key}」對應多個知識點，使用最相關的一個：{hits[0]['id']}\n", file=sys.stderr)
    return hits[0]


def search(query):
    terms = query.lower().split()
    scored = []
    for n in G["nodes"]:
        fields = [(n["label"], 6), (n["en"], 4), (" ".join(n["tags"]), 4),
                  (n["id"], 3), (n["desc"], 2), (n["code"] or "", 1)]
        total = 0
        for t in terms:
            s = sum(w for f, w in fields if t in f.lower())
            if not s:
                total = 0
                break
            total += s
        if total:
            scored.append((total, n))
    scored.sort(key=lambda x: -x[0])
    return [n for _, n in scored]


def cmd_search(a):
    hits = search(" ".join(a.query))
    if not hits:
        print("沒有符合的知識點。")
    for n in hits[: a.limit]:
        mark = " *程式*" if n["code"] else ""
        print(f"Ch0{n['chapter']}  {tag(n)}{mark}")


def cmd_show(a):
    n = resolve(a.id)
    print("=" * 72)
    print(tag(n))
    if n["en"]:
        print("   ", n["en"])
    print("=" * 72)
    if n["desc"]:
        print(n["desc"], "\n")
    if n["tags"]:
        print("標籤：", "、".join(n["tags"]))
    for r in n["refs"]:
        print("參考：", r)
    if n["code"]:
        origin = "參考解答 (非講義原文)" if n["source"] == "solution" else "講義程式"
        print(f"\n--- 程式碼 ({origin}) " + "-" * 40)
        print(n["code"])
        print("-" * 60)
        if n["stdin"]:
            print("範例輸入：", " / ".join(n["stdin"]))
    print()
    for rel, (o, i) in REL_TEXT.items():
        outs = [e["target"] for e in OUT[n["id"]] if e["rel"] == rel]
        ins = [e["source"] for e in INC[n["id"]] if e["rel"] == rel]
        if rel == "related":
            outs, ins = sorted(set(outs + ins)), []
        for title, ids in ((o, outs), (i, ins)):
            if ids:
                print(f"{title}：")
                for x in ids:
                    print("   -", tag(NODES[x]))


def cmd_code(a):
    n = resolve(a.id)
    if not n["code"]:
        sys.exit(f"{n['id']} 沒有程式碼")
    print(n["code"])


def cmd_run(a):
    n = resolve(a.id)
    if not n["code"] or n["lang"] != "python":
        sys.exit(f"{n['id']} 沒有可執行的 Python 程式")
    print(f">>> 執行 {tag(n)}\n")
    exec(compile(n["code"], n["id"], "exec"), {"__name__": "__main__"})


def cmd_tree(a):
    start = resolve(a.id) if a.id else NODES["root"]

    def walk(i, depth):
        n = NODES[i]
        mark = " *" if n["code"] else ""
        print("  " * depth + ("└ " if depth else "") + f"{n['label']}{mark}  ({i})")
        for e in OUT[i]:
            if e["rel"] == "contains":
                walk(e["target"], depth + 1)

    walk(start["id"], 0)
    print("\n(* 表示有程式碼)")


def cmd_path(a):
    src, dst = resolve(a.src)["id"], resolve(a.dst)["id"]
    adj = collections.defaultdict(list)
    for e in G["edges"]:
        if e["source"] == "root" or e["target"] == "root":
            continue  # 避免所有路徑都經過根節點
        adj[e["source"]].append((e["target"], e["rel"], True))
        adj[e["target"]].append((e["source"], e["rel"], False))
    prev = {src: None}
    q = collections.deque([src])
    while q:
        cur = q.popleft()
        if cur == dst:
            break
        for nxt, rel, fwd in adj[cur]:
            if nxt not in prev:
                prev[nxt] = (cur, rel, fwd)
                q.append(nxt)
    if dst not in prev:
        sys.exit("兩個知識點之間沒有路徑。")
    chain = []
    cur = dst
    while prev[cur]:
        p, rel, fwd = prev[cur]
        chain.append((p, rel, fwd, cur))
        cur = p
    print(tag(NODES[src]))
    for p, rel, fwd, c in reversed(chain):
        word = REL_TEXT[rel][0 if fwd else 1]
        print(f"   --{word}--> {tag(NODES[c])}")


def cmd_list(a):
    for n in G["nodes"]:
        if n["kind"] == a.kind and (a.chapter is None or n["chapter"] == a.chapter):
            print(f"Ch0{n['chapter']}  {tag(n)}")


def cmd_stats(_):
    c = collections.Counter(n["kind"] for n in G["nodes"])
    r = collections.Counter(e["rel"] for e in G["edges"])
    print("知識點：", len(G["nodes"]), {KINDS[k]: v for k, v in c.items()})
    print("關係  ：", len(G["edges"]), {G["meta"]["relations"][k]: v for k, v in r.items()})
    print("程式碼：", sum(1 for n in G["nodes"] if n["code"]))


def main(argv=None):
    _fix_stdout()
    p = argparse.ArgumentParser(description="Python 知識圖譜查詢工具 (PyML Ch01–Ch05)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="關鍵字搜尋")
    s.add_argument("query", nargs="+")
    s.add_argument("-n", "--limit", type=int, default=20)
    s.set_defaults(f=cmd_search)
    for name, f, h in (("show", cmd_show, "顯示知識點"), ("code", cmd_code, "輸出程式碼"),
                       ("run", cmd_run, "執行程式")):
        s = sub.add_parser(name, help=h)
        s.add_argument("id", help="知識點 id 或關鍵字")
        s.set_defaults(f=f)
    s = sub.add_parser("tree", help="章節樹狀結構")
    s.add_argument("id", nargs="?")
    s.set_defaults(f=cmd_tree)
    s = sub.add_parser("path", help="兩個知識點之間的路徑")
    s.add_argument("src")
    s.add_argument("dst")
    s.set_defaults(f=cmd_path)
    s = sub.add_parser("list", help="依類型列出")
    s.add_argument("kind", choices=[k for k in KINDS if k != "root"])
    s.add_argument("chapter", nargs="?", type=int)
    s.set_defaults(f=cmd_list)
    s = sub.add_parser("stats", help="統計")
    s.set_defaults(f=cmd_stats)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
