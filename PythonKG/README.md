# Python 程式設計 知識圖譜 (PyML Ch01–Ch05)

將 C. Alex Hu, PhD《Python 程式設計》講義第 1–5 章整理成可查詢的知識圖譜，
每個觀念、範例與習題都附上可執行的程式碼。

| 章 | 主題 |
|----|------|
| Ch01 | Python 介紹、Anaconda / Miniconda、conda 虛擬環境、Google Colab |
| Ch02 | int / float / complex、算術運算、Decimal、Fraction、字串、bytes、索引與切片 |
| Ch03 | if / elif、while、for、range、break / continue / for-else；GCD、費氏數列、二元搜尋、蒙地卡羅、質數、氣泡排序、樂透 |
| Ch04 | 序列運算、list 方法、Stack、List Comprehension、tuple packing / unpacking、enumerate、zip、str 方法 |
| Ch05 | set、frozenset、dict、Set / Dict Comprehension、字數統計 |

圖譜共 **104 個知識點、281 條關係、82 段程式**
(講義範例程式 + 22 題習題的參考解答，解答會標示「非講義原文」)。

## 檔案

| 檔案 | 用途 |
|------|------|
| `index.html` | 互動式知識圖譜網頁，直接用瀏覽器開啟 (資料已內嵌) |
| `kg.py` | 命令列查詢工具：搜尋、顯示、輸出程式、執行、路徑查詢 |
| `programs/chNN/*.py` | 每段程式各自一個 `.py` 檔，可直接執行或在 Jupyter 中貼上 |
| `knowledge_graph.json` | 圖譜資料 (節點、關係、程式碼、範例執行結果)，可匯入其他工具 |
| `kg_data.py` | 圖譜的原始資料：要新增或修改知識點請改這裡 |
| `build.py` | 由 `kg_data.py` 重新產生 JSON、HTML 與 programs/ |
| `test_kg.py` | 檢查圖譜結構，並執行所有程式確認沒有錯誤 |

## 網頁 (`index.html`)

- 左側：關鍵字搜尋 (中文、英文、程式碼內容都可搜)，依類型與章節篩選
- 中間：知識圖譜，點選節點會標出它的所有關聯；滾輪縮放、拖曳平移
- 右側：說明、程式碼 (一鍵複製)、範例執行結果、相關知識點

可用網址 hash 直接開啟某個知識點，例如 `index.html#ex-gcd`。
關係圖需要連網載入 D3；離線時搜尋、內容與程式碼仍可使用。

## 命令列 (`kg.py`)

```bash
python kg.py search 切片            # 關鍵字搜尋
python kg.py show c_slicing          # 知識點說明 + 程式碼 + 所有關係
python kg.py code ex_bsearch > sqrt.py   # 只輸出程式碼
python kg.py run q3_5                # 直接執行 (立方根，二元搜尋法)
python kg.py tree ch4                # 第 4 章樹狀結構
python kg.py path ex_lotto q5_2      # 兩個知識點之間的關聯路徑
python kg.py list exercise 5         # 列出第 5 章所有習題
python kg.py stats
```

`show` / `code` / `run` 也接受關鍵字，例如 `python kg.py run 氣泡排序`。

## 節點與關係

節點類型：章 `chapter`、節 `section`、觀念 `concept`、函式 / 方法 `function`、
範例 `example`、習題 `exercise`。

關係類型：

| 關係 | 意義 | 例子 |
|------|------|------|
| `contains` 包含 | 章節 / 觀念的階層 | Ch03 → while 迴圈 → GCD 範例 |
| `uses` 使用 | 範例用到哪些觀念 | 二元搜尋 → Decimal |
| `related` 相關 | 互相對照的觀念 | List / Set / Dict Comprehension |
| `refactors` 改寫自 | 同一問題的精簡版 | List Comprehension 找質數 → 解法一 |
| `practice` 練習 | 習題對應的範例 | Exercise 3.6 → 樂透、氣泡排序 |
| `prereq` 前置 | 章節學習順序 | Ch02 → Ch03 |

## 新增或修改

1. 編輯 `kg_data.py`，用 `node(...)` 新增知識點 (`parent=` 決定掛在哪一節，
   `uses=` / `related=` / `practice=` 建立關係，`code=` 放程式，
   需要 `input()` 的程式用 `stdin=[...]` 提供範例輸入)。
2. 執行 `python build.py`。
3. 執行 `python -m pytest test_kg.py` 確認所有程式都能跑。
