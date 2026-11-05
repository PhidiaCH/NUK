# -*- coding: utf-8 -*-
"""
產生知識圖譜輸出檔：
  knowledge_graph.json   圖譜資料 (節點、關係、程式碼、範例執行結果)
  index.html             互動式知識圖譜網頁 (資料已內嵌，可直接用瀏覽器開啟)
  programs/chNN/*.py     每段程式各自輸出成可執行的 .py 檔

用法：python build.py
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kg_data import build_graph  # noqa: E402
from runner import run_code  # noqa: E402

MAX_OUTPUT = 4000


def attach_outputs(graph):
    """執行每段 Python 程式，把範例輸出存進節點 (run_output)。"""
    failures = []
    for n in graph["nodes"]:
        n["run_output"] = None
        if not n["code"] or n["lang"] != "python":
            continue
        text, err = run_code(n["code"], n["stdin"])
        if err is not None:
            failures.append(f"{n['id']}: {err!r}")
        text = text.rstrip()
        if len(text) > MAX_OUTPUT:
            text = text[:MAX_OUTPUT] + "\n… (輸出過長，已截斷)"
        n["run_output"] = text or None
    return failures


def write_programs(graph, root):
    """把每段程式寫成 programs/chNN/<id>.py，並附上標題註解。"""
    count = 0
    for n in graph["nodes"]:
        if not n["code"]:
            continue
        ext = ".py" if n["lang"] == "python" else ".sh"
        folder = root / f"ch{n['chapter']:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        origin = "參考解答 (非講義原文)" if n["source"] == "solution" else "講義程式"
        header = [f"# {n['label']}", f"# 知識點 id: {n['id']}  |  {origin}"]
        if n["stdin"]:
            header.append("# 範例輸入: " + " / ".join(n["stdin"]))
        body = "\n".join(header) + "\n\n" + n["code"] + "\n"
        if ext == ".py":
            body = "# -*- coding: utf-8 -*-\n" + body
        (folder / (n["id"] + ext)).write_text(body, encoding="utf-8")
        count += 1
    return count


def render_html(graph, standalone=True):
    template = (HERE / "template.html").read_text(encoding="utf-8")
    data = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")  # 避免程式碼中的 </script> 提前結束標籤
    page = template.replace("/*__KG_DATA__*/null", data)
    if standalone:
        page = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                "</head>\n<body>\n" + page + "\n</body>\n</html>\n")
    return page


def main():
    graph = build_graph()
    failures = attach_outputs(graph)
    (HERE / "knowledge_graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "index.html").write_text(render_html(graph), encoding="utf-8")
    n_prog = write_programs(graph, HERE / "programs")
    print(f"nodes={len(graph['nodes'])} edges={len(graph['edges'])} programs={n_prog}")
    if failures:
        print("執行失敗的程式：\n  " + "\n  ".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
