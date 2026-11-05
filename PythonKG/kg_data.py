# -*- coding: utf-8 -*-
"""
PyML 講義 Ch01–Ch05 知識圖譜資料 (Knowledge Graph Data)

來源：C. Alex Hu, PhD —《Python 程式設計》PyML Ch01 ~ Ch05
  Ch01 Python 程式語言介紹與環境建置
  Ch02 Python 資料型別與基本運算
  Ch03 流程控制
  Ch04 資料結構一：內建的序列資料型別 (list / tuple / str / bytes)
  Ch05 資料結構二：set / frozenset / dictionary

節點 (node) 種類：
  chapter  章            section  節
  concept  觀念 / 語法    function 內建函式 / 方法
  example  講義範例 (含程式)
  exercise 習題 (含參考解答程式，非講義原文)

關係 (edge) 種類：
  contains  包含        uses      使用到
  related   相關        refactors 改寫 / 精簡自
  practice  練習        prereq    前置知識

執行 `python build.py` 會輸出 knowledge_graph.json 與 index.html。
"""
from textwrap import dedent

NODES = []
EDGES = []
_IDS = set()


def _code(s):
    if s is None:
        return None
    return dedent(s).strip("\n")


def node(id, kind, label, chapter, parent=None, desc="", code=None, output=None,
         uses=(), related=(), refactors=(), prereq=(), practice=(),
         tags=(), refs=(), stdin=None, slow=False, lang="python",
         source=None, en=""):
    """新增一個節點，並依參數自動建立關係邊。"""
    assert id not in _IDS, f"duplicate id: {id}"
    _IDS.add(id)
    if source is None:
        source = "solution" if kind == "exercise" else "lecture"
    NODES.append(dict(
        id=id, kind=kind, label=label, en=en, chapter=chapter,
        desc=dedent(desc).strip(), code=_code(code), output=_code(output),
        lang=lang, tags=list(tags), refs=list(refs),
        stdin=list(stdin) if stdin else None, slow=slow, source=source,
    ))
    if parent:
        EDGES.append((parent, id, "contains"))
    for t in uses:
        EDGES.append((id, t, "uses"))
    for t in related:
        EDGES.append((id, t, "related"))
    for t in refactors:
        EDGES.append((id, t, "refactors"))
    for t in prereq:
        EDGES.append((t, id, "prereq"))
    for t in practice:
        EDGES.append((id, t, "practice"))


def edge(a, b, rel="related"):
    EDGES.append((a, b, rel))


# ============================================================================
# 根節點
# ============================================================================
node("root", "root", "Python 程式設計 (PyML Ch01–05)", 0,
     desc="C. Alex Hu, PhD 講義《Python 程式設計》第 1–5 章的知識圖譜。"
          "從環境建置、資料型別、流程控制，到序列 / 非序列資料結構。")

# ============================================================================
# Ch01 Python 程式語言介紹與環境建置
# ============================================================================
node("ch1", "chapter", "Ch01 Python 介紹與環境建置", 1, parent="root",
     en="Intro to Python Programming",
     desc="Python 官方資源、Anaconda / Miniconda 安裝、conda 虛擬環境與 Google Colab。")

node("s1_1", "section", "1.1 Python 程式語言介紹", 1, parent="ch1",
     desc="Python 官方網站、下載頁面與 Python 3 官方文件。",
     refs=["https://www.python.org", "https://www.python.org/downloads",
           "https://docs.python.org/3/"])

node("s1_2", "section", "1.2 安裝 Anaconda", 1, parent="ch1",
     desc="""
     STEP 1 連線至 Anaconda 下載網頁。
     STEP 2 下載 Anaconda Individual Edition 並安裝。
     STEP 3 啟動 Anaconda Navigator → Jupyter Notebook。""",
     refs=["https://www.anaconda.com/download"], tags=["安裝", "Jupyter"])

node("s1_3", "section", "1.3 安裝 Miniconda 與虛擬環境", 1, parent="ch1",
     desc="""
     下載適合平台 (Windows / macOS / Linux) 的 Miniconda，
     開啟 Anaconda Prompt (miniconda3) 後以 conda 指令建立並使用虛擬環境。""",
     refs=["https://docs.anaconda.com/free/miniconda/",
           "https://conda.io/projects/conda/en/latest/user-guide/getting-started.html"],
     lang="bash", tags=["conda", "虛擬環境", "安裝"],
     code="""
     # 1. 建立虛擬環境 (例如 minienv)
     conda create -n minienv
     # 2. 查看虛擬環境
     conda info --envs
     # 3. 啟動虛擬環境
     conda activate minienv
     # 4. 在虛擬環境中安裝 Python
     conda install python
     # 5. 安裝 NumPy, Pandas, matplotlib
     conda install numpy pandas matplotlib
     # 6. 安裝 Jupyter Notebook
     conda install jupyter
     # 7. 執行 Jupyter Notebook
     jupyter notebook
     """)

node("c_conda_env", "concept", "conda 虛擬環境", 1, parent="s1_3",
     en="conda virtual environment",
     desc="以 conda create / activate 建立互相隔離的 Python 執行環境，"
          "每個環境可安裝不同版本的套件。",
     tags=["conda", "環境"])

node("s1_4", "section", "1.4 Google Colaboratory", 1, parent="ch1",
     desc="免安裝、在瀏覽器中執行 Jupyter Notebook 的雲端環境。",
     refs=["https://colab.research.google.com/notebooks/intro.ipynb"])

node("c_jupyter", "concept", "Jupyter Notebook", 1, parent="ch1",
     desc="互動式筆記本：以 In [n] / Out[n] 儲存格逐段執行 Python。"
          "最後一個運算式的值會自動顯示，並存入內建變數 _ 。",
     related=["s1_2", "s1_4"], tags=["環境"])

# ============================================================================
# Ch02 Python 資料型別與基本運算
# ============================================================================
node("ch2", "chapter", "Ch02 資料型別與基本運算", 2, parent="root",
     en="Python Datatypes and Basic Operations",
     desc="Python 是直譯式 (interpreter) 語言，由 Guido van Rossum 於 1989 年開發，"
          "名稱來自 BBC 節目 Monty Python's Flying Circus。本章介紹數值與字串運算。",
     refs=["https://docs.python.org/3/tutorial/appetite.html"],
     prereq=["ch1"])

node("s2_1", "section", "2.1 數值運算", 2, parent="ch2", en="Numeric Operations",
     desc="Python 的數值型別：int、float、complex，以及標準函式庫的 Decimal 與 Fraction。")

node("c_literal", "concept", "常值與資料物件", 2, parent="s2_1",
     en="Literals / Data in Python",
     desc="Python 常值是一個物件，包含指向記憶體位址的指標，以及資料型別、大小與資料值。",
     refs=["https://jakevdp.github.io/PythonDataScienceHandbook/02.01-understanding-data-types.html"],
     code="""
     print(10)        # a constant integer number
     print(3.1415)    # a constant floating value
     print(3 + 5j)    # a constant complex number
     print(type(10), type(3.1415), type(3 + 5j))
     """)

node("c_int", "concept", "int 整數", 2, parent="s2_1", en="int",
     desc="任意精度整數。", related=["c_literal"], tags=["數值型別"])
node("c_float", "concept", "float 浮點數", 2, parent="s2_1", en="float",
     desc="二進位浮點數 (binary floating-point)，十進位轉換時可能有精度誤差，"
          "例如 1.41421 ** 2 = 1.9999899240999999。",
     related=["c_literal", "c_decimal"], tags=["數值型別"])
node("c_complex", "concept", "complex 複數", 2, parent="s2_1", en="complex",
     desc="以 j 表示虛部，例如 3 + 5j。", related=["c_literal"], tags=["數值型別"])

node("c_arith", "concept", "算術運算子", 2, parent="s2_1",
     en="Arithmetic operators + - * / // % **",
     desc="""
     +  加、-  減、*  乘
     /  除法：結果一定是 float
     // 整數除法 (floor division)
     %  餘數 (modulus)
     ** 次方""",
     uses=["c_int", "c_float"],
     code="""
     print(22 + 28)             # 50
     print(150 - 5*26)          # 20
     print((150 - 5*26) / 5)    # 4.0  除法一定回傳 float
     print(80 / 5)              # 16.0
     print(79 // 3)             # 26   floor division
     print(79 % 3)              # 1    modulus
     print(1.41421 ** 2)        # 1.9999899240999999
     print(10 ** 3)             # 1000
     """)

node("c_typeconv", "function", "int() / float() 型別轉換", 2, parent="s2_1",
     en="Type conversion",
     desc="int() 會截去小數部分；float() 將整數轉為浮點數。",
     uses=["c_int", "c_float"],
     code="""
     print(int(2023 - 4 * 25.0))   # 1923
     print(5 * 3.21)               # 16.05
     print(int(5 * 3.21))          # 16
     print(float(2023))            # 2023.0
     """)

node("c_variable", "concept", "變數與指定運算子 =", 2, parent="s2_1",
     en="Variables & assignment",
     desc="""
     lValue = rValue
     rValue (右值)：資料值，例如 10, 100.0, 'Hello world', True
     lValue (左值)：位址 / 名稱，例如 x, myObject
     Python 的變數是「名稱綁定到物件」，與 C/C++ 的「變數是一塊記憶體」不同。
     互動模式下，最後輸出的運算式值會存在內建變數 _ 中。""",
     related=["c_jupyter"],
     code="""
     interest_rate = 0.06
     capital = 1000000
     growth = (1 + interest_rate) ** 32   # Notebook 中可寫成 _ ** 32
     print(growth)                        # 6.4533866818853385
     print(capital * growth)              # 6453386.681885338
     """)

node("c_decimal", "concept", "Decimal 十進位精確運算", 2, parent="s2_1",
     en="decimal.Decimal",
     desc="""
     decimal 模組提供十進位定點 / 浮點運算，可用 getcontext().prec 設定有效位數。
     注意：Decimal 的 % 結果正負號跟隨「被除數」，// 向 0 取整；
     int 的 % 正負號跟隨「除數」，// 向下取整。""",
     refs=["https://docs.python.org/3/library/decimal.html"],
     tags=["精度", "標準函式庫"],
     code="""
     from decimal import Decimal
     print((-15) % 4)                    # 1
     print((-15) // 4)                   # -4
     print(Decimal(-15) % Decimal(4))    # -3
     print(Decimal(-15) // Decimal(4))   # -3
     """)

node("ex_golden", "example", "範例：黃金比例 (Golden Ratio)", 2, parent="s2_1",
     desc="""
     黃金比例 = (1 + √5) / 2 = 1.6180339887498948482…
     利用費氏數列連續二數比值 F(n+1)/F(n) 趨近黃金比例，
     以 Decimal 計算到小數點後第 30 位。""",
     uses=["c_decimal", "c_while", "c_tuple_unpacking"], related=["ex_fib"],
     tags=["Fibonacci", "精度", "演算法"],
     code="""
     from decimal import Decimal, getcontext
     getcontext().prec = 50   # 設定最大有效位數
     n = 30                   # 精確至小數點後第 30 位

     a, b, count = 1, 1, 0
     # < Method 1 > : count = 73 for n = 30
     # while (round(Decimal(str(1+a/b)),n) - round(Decimal(str(b/a)),n)) != 0:
     # < Method 2 > : count = 74 for n = 30
     while abs(Decimal(str(1+a/b))/Decimal(str(b/a)) - Decimal('1.0')) > 0.1**(n+1):
         a, b, count = Decimal(str(b)), Decimal(str(a+b)), count+1

     print('n = ', n, ' count = ', count, ': \\t a =', a, '\\t b =', b)
     print('精確至第', n, '位數 :\\t b/a = \\t', Decimal(str(b/a)))
     print('精確至第', n, '位數 :\\t (a+b)/b = \\t', Decimal(str(1+a/b)))
     print('精確至第 50 位數 : Correct Answer = \\t',
           Decimal('1.61803398874989484820458683436563811772030917980576'))
     """,
     output="""
     n =  30  count =  74 : 	 a = 2111485077978050 	 b = 3416454622906707
     精確至第 30 位數 :	 b/a = 	 1.6180339887498948482045868343655378089365420345661
     精確至第 30 位數 :	 (a+b)/b = 	 1.6180339887498948482045868343656764322663380655694
     """)

node("c_fraction", "concept", "Fraction 分數", 2, parent="s2_1",
     en="fractions.Fraction",
     desc="以「整數 / 整數」表示有理數。Fraction 繼承抽象類別 numbers.Rational。"
          "注意 Fraction(3.33) 會得到 float 的精確二進位值，"
          "Fraction(Decimal('3.33')) 或 Fraction('3.33') 才是 333/100。",
     refs=["https://docs.python.org/3/library/fractions.html"],
     related=["c_decimal", "c_float"], tags=["標準函式庫"],
     code="""
     from fractions import Fraction
     from decimal import Decimal
     print(Fraction(30, -4))          # -15/2
     print(Fraction(2018))            # 2018
     print(Fraction())                # 0
     print(Fraction('4/23'))          # 4/23
     print(Fraction('1.41421'))       # 141421/100000
     print(Fraction('-.125'))         # -1/8
     print(Fraction('1.7e-3'))        # 17/10000
     print(Fraction(3.33))            # 1874623344892969/562949953421312
     print(Fraction(Decimal('3.33'))) # 333/100
     """)

node("q2_golden_int", "exercise", "Q：不用 Decimal 計算黃金比例至 30 位", 2,
     parent="s2_1",
     desc="講義提問：是否可以不用 Decimal 來計算黃金比例至小數點後 30 位？"
          "參考解答：Python 的 int 為任意精度，可把比值放大 10**k 倍後用整數除法 // 計算。",
     uses=["c_int", "c_arith", "c_while"], practice=["ex_golden"],
     code="""
     n = 30
     SCALE = 10 ** (n + 5)            # 多保留 5 位當保護位數

     a, b, count = 1, 1, 0
     prev = None
     while True:
         a, b = b, a + b              # 費氏數列
         count += 1
         ratio = b * SCALE // a       # 以整數運算取得放大後的比值
         digits = ratio // 10**5      # 截到小數點後 n 位
         if digits == prev:           # 連續兩次在第 n 位相同 → 收斂
             break
         prev = digits

     s = str(digits)
     print('count =', count, ' a =', a, ' b =', b)
     print('黃金比例 ≈', s[0] + '.' + s[1:])
     # 1.618033988749894848204586834365
     """)

node("s2_2", "section", "2.2 字串運算", 2, parent="ch2", en="String Operations",
     desc="字串常值、跳脫字元、raw string、三重引號、串接與重複、bytes、索引與切片。")

node("c_str", "concept", "str 字串常值", 2, parent="s2_2", en="String literals",
     desc="""
     單引號 '...' 或雙引號 "..." 皆可。
     \\' 跳脫單引號；\\n 換行。
     r'...' raw string：不處理跳脫字元 (常用於 Windows 路徑)。
     \"\"\"...\"\"\" 或 '''...''' 三重引號可跨多行。""",
     tags=["字串"],
     code='''
     print('Hello Python!')
     print('isn\\'t')                 # 跳脫字元
     print("isn't")                    # 改用雙引號
     print('"No, it isn\\'t," he said.')
     string = 'Hello, Alice.\\nHi, Bob. How are you?'
     print(string)                     # \\n 產生換行
     print('C:\\Python\\notebook')      # \\n 被當成換行!
     print(r'C:\\Python\\notebook')     # raw string
     print("""\\
     [Agenda]
      9:00 ~ 9:30  Reception
      9:30 ~ 10:20 Keynote Speech
     """)
     ''')

node("c_str_concat", "concept", "字串串接 + 與重複 *", 2, parent="s2_2",
     en="Concatenation & repetition",
     desc="+ 串接、* 重複。相鄰的字串常值會自動串接；"
          "但變數與常值相鄰 (string \"Python\") 會產生 SyntaxError。",
     uses=["c_str"], related=["c_seq_ops"],
     code="""
     print('repe' + 'ti'*2 + 'on')        # repetition
     print('He' 'llo' ' Python')           # 相鄰常值自動串接
     string = "Fly Robin Fly" " Up Up To The Sky"
     print(string)
     # string "Python"   # SyntaxError: 變數不能與常值自動串接
     """)

node("c_bytes", "concept", "bytes 位元組常值", 2, parent="s2_2",
     en="Bytes literals",
     desc="語法與字串相同但加上 b 字首；只能包含 ASCII 字元 (0–127)，"
          "大於 127 的值需用跳脫序列。bytes 是不可改變的序列。",
     refs=["https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview"],
     related=["c_str", "c_immutable"], tags=["字串"],
     code="""
     bytes_string = b'Hello Python!'
     print(bytes_string)                              # b'Hello Python!'
     print(str(bytes_string))                         # "b'Hello Python!'"
     print(str(bytes_string, encoding='UTF-8'))       # bytes → str
     print(bytes('Hi there!', encoding='ASCII'))      # str → bytes
     """)

node("c_indexing", "concept", "Indexing 索引", 2, parent="s2_2", en="Indexing",
     desc="序列資料 (str / list / tuple) 以索引標示元素位置；第一個元素索引為 0，"
          "負索引從尾端往前數 (-1 為最後一個)。超出範圍會產生 IndexError。"
          "id() 可回傳物件的記憶體位址。",
     related=["c_sequence"], tags=["序列"],
     code="""
     text = 'Hello Python!'
     print(text[0], text[3], text[12])   # H l !
     print(text[-1], text[-7])           # ! P
     print(repr(text[-8]))               # ' '
     print(text[-0])                     # H
     print(id(text[0]), id(text))        # id(): 物件的記憶體位址
     # text[20]  # IndexError: string index out of range
     """)

node("c_slicing", "concept", "Slicing 切片", 2, parent="s2_2",
     en="Slicing  seq[start:stop:step]",
     desc="seq[start:stop:step]：包含 start、不包含 stop；預設 [0 : 尾端 : 1]。"
          "切片超出範圍不會出錯，只會回傳較短 (或空) 的結果。",
     uses=["c_indexing"], tags=["序列"],
     code="""
     text = 'Hello Python!'
     print(text[:5])        # 'Hello'
     print(text[3:])        # 'lo Python!'
     print(text[3:20])      # 'lo Python!'
     print(repr(text[20:])) # ''  empty string
     print(text[-1:1:-1])   # '!nohtyP oll'
     print(text[:6] + 'world!')        # 'Hello world!'
     print(text[6:10] + 'agoras')      # 'Pythagoras'
     """)

node("c_immutable", "concept", "可變 vs 不可變 (mutable / immutable)", 2, parent="s2_2",
     en="Mutability",
     desc="""
     不可變 (immutable)：int, float, str, bytes, tuple, frozenset
       → 不能修改元素，例如 text[5] = 's' 會產生 TypeError。
     可變 (mutable)：list, set, dict
       → 可以就地 (in-place) 修改。
     只有 immutable 物件可以當 dict 的 key 或 set 的元素。""",
     tags=["核心觀念"],
     code="""
     text = 'Hello Python!'
     try:
         text[5] = 's'
     except TypeError as e:
         print('TypeError:', e)   # 'str' object does not support item assignment
     print(text[:5] + 's' + text[6:])   # 改用切片產生新字串
     """)

node("f_len", "function", "len()", 2, parent="s2_2", en="len()",
     desc="回傳序列 (或集合、字典) 的元素個數。",
     code="""
     text = 'Hello Python!'
     print(len(text))     # 13
     """)

node("f_str", "function", "str()", 2, parent="s2_2", en="str()",
     desc="將物件轉為字串。",
     code="""
     print(str(1000))         # '1000'
     print(str(3.1415926))    # '3.1415926'
     """)

# ============================================================================
# Ch03 流程控制
# ============================================================================
node("ch3", "chapter", "Ch03 流程控制", 3, parent="root", en="Flow Control",
     desc="if / elif / else、while、for、range()、break / continue / pass，"
          "以及 GCD、費氏數列、二元搜尋、蒙地卡羅、質數、氣泡排序、樂透選號等演算法。",
     refs=["https://docs.python.org/3/tutorial/index.html"], prereq=["ch2"])

node("c_if", "concept", "if / elif / else", 3, parent="ch3",
     en="if statement",
     desc="elif 是 else if 的縮寫，可避免過多縮排。Python 以縮排 (indentation) 區分程式區塊。",
     stdin=["0.5"],
     code="""
     x = float(input("Please enter a number: "))
     if x < 0:
         print(x, 'is less than zero !')
     elif x == 0:
         print('0')
     elif x == 1:
         print('1')
     else:
         print(x, ' > 0')
     """)

node("c_compare", "concept", "比較運算子", 3, parent="ch3",
     en="Comparison operators",
     desc="<  >  ==  <=  >=  !=  與 C/C++ 相同。"
          "非 0 數值為 True、0 為 False；非空序列為 True、空序列為 False。",
     related=["c_if", "c_while", "c_set_compare"])

node("c_while", "concept", "while 迴圈", 3, parent="ch3", en="while loop",
     desc="""
     while [condition]:
         [body]
     只要條件為真就持續執行；迴圈次數不確定時通常使用 while。""",
     uses=["c_compare"],
     code="""
     n = 0
     while n < 5:
         print(n, end=' ')
         n += 1
     """)

node("ex_gcd", "example", "範例：最大公因數 GCD (輾轉相除法)", 3, parent="c_while",
     desc="最大公因數演算法是人類發現的第一個演算法 (Euclid)。",
     uses=["c_while", "c_tuple_unpacking", "c_arith"], tags=["演算法"],
     code="""
     # GCD: greatest common divisor
     (a, b) = (21, 144)
     while a != 0:
         print(' a =\\t', a, '\\t b =\\t', b)
         a, b = b % a, a
     print(" GCD = ", b)
     """,
     output="""
      a =	 21 	 b =	 144
      a =	 18 	 b =	 21
      a =	 3 	 b =	 18
      GCD =  3
     """)

node("ex_fib", "example", "範例：費氏數列 Fibonacci", 3, parent="c_while",
     desc="F(n+2) = F(n) + F(n+1)，F0 = 0, F1 = 1。",
     uses=["c_while", "c_tuple_unpacking"], tags=["演算法", "Fibonacci"],
     code="""
     a, b = 0, 1
     print('Fibonacci numbers = ', a, end=' ')
     while b < 50:
         print(b, end=' ')
         a, b = b, a+b
     # 0 1 1 2 3 5 8 13 21 34
     """)

node("q3_gcd_input", "exercise", "練習：任意輸入 a, b 計算 GCD 與費氏數列", 3,
     parent="c_while", practice=["ex_gcd", "ex_fib"], stdin=["21", "144", "100"],
     desc="修改 GCD 與費氏數列程式，使其可以任意輸入數值。",
     code="""
     def gcd(a, b):
         while a != 0:
             a, b = b % a, a
         return abs(b)

     def fibonacci(limit):
         a, b, seq = 0, 1, [0]
         while b < limit:
             seq.append(b)
             a, b = b, a + b
         return seq

     a = int(input('a = '))
     b = int(input('b = '))
     print('GCD(%d, %d) = %d' % (a, b, gcd(a, b)))
     limit = int(input('費氏數列上限 = '))
     print('Fibonacci <', limit, ':', fibonacci(limit))
     """)

node("ex_bsearch", "example", "範例：二元搜尋法求平方根", 3, parent="c_while",
     en="Binary Search Algorithm",
     desc="以上下界逼近：mid² ≥ a 則 upper = mid，否則 lower = mid，"
          "直到上下界在小數點後 n 位相同。用 Decimal 避免 float 精度問題。",
     uses=["c_while", "c_decimal", "c_if"], tags=["演算法", "二元搜尋"],
     stdin=["2"],
     code="""
     from math import trunc
     from decimal import Decimal, getcontext
     getcontext().prec = 31   # 最大精度至小數點後第 30 位
     n = 25                   # 問題精度：小數點後第 25 位

     a = float(input("Enter a positive number: "))
     if a < 0:
         raise ValueError(' **** a = %s : < 0: ERROR !! ' % a)

     lower, upper = 0, a
     if a < 1: upper = 1

     while round(Decimal(str(upper)), n) != round(Decimal(str(lower)), n):
         avg = (Decimal(str(upper)) + Decimal(str(lower))) / Decimal('2')
         if avg**2 >= Decimal(str(a)):
             upper = avg
         else:
             lower = avg

     sol = Decimal(str(trunc(upper * 10**n))) / Decimal(str(10**n))
     print(' Upper of Square Root =', upper)
     print(' Lower of Square Root =', lower)
     print(a, '的平方根，精確至小數點後第', n, '位 :')
     print(' squareRoot(', a, ') =', sol)
     # squareRoot( 2.0 ) = 1.4142135623730950488016887
     """)

node("ex_montecarlo", "example", "範例：蒙地卡羅法估算圓周率 π", 3, parent="c_while",
     en="Monte Carlo method",
     desc="在單位正方形內隨機撒點，落在 1/4 圓內的比例 ≈ π/4。"
          "seed() 固定亂數種子 → 結果可重現。講義使用 10**8 點 (π ≈ 3.14186)；"
          "此處預設 10**6 點以加快執行。",
     uses=["c_while", "c_if"], tags=["演算法", "亂數"],
     code="""
     from random import random, seed
     from math import sqrt

     total = 10**6     # 講義原為 10**8
     seed(100)         # 固定亂數種子 => 固定亂數輸出值

     i = count = 0
     while i < total:
         i += 1
         x, y = random(), random()     # 亂數值介於 [0, 1)
         if sqrt(x**2 + y**2) <= 1.0:  # Euclidean distance
             count += 1

     pi = 4 * count / total            # 圓內點數 : 總點數 = π : 4
     print('Pi = {:.5f}'.format(pi))
     """)

node("q3_5", "exercise", "Exercise 3.5 二元搜尋法求立方根 (正、負、0)", 3,
     parent="c_while", practice=["ex_bsearch"],
     uses=["c_decimal", "c_while"],
     desc="利用二元搜尋計算實數 a 的立方根，精確至小數點後第 50 位 (a 可 > 0、= 0、< 0)。"
          "提示：程式碼重用 (reusability) — 寫成函式，負數取 -cbrt(-a)。",
     code="""
     from decimal import Decimal, getcontext, ROUND_DOWN

     def cube_root(a, n=50):
         getcontext().prec = n + 20
         a = Decimal(str(a))
         if a == 0:
             return Decimal(0)
         if a < 0:                          # 負數：利用奇函數性質
             return -cube_root(-a, n)
         lower, upper = Decimal(0), max(a, Decimal(1))
         eps = Decimal(10) ** -(n + 5)
         while upper - lower > eps:
             mid = (lower + upper) / 2
             if mid ** 3 >= a:
                 upper = mid
             else:
                 lower = mid
         return upper.quantize(Decimal(10) ** -n, rounding=ROUND_DOWN)

     for a in (27, 2, 0, -8, -2, 0.001):
         print('cbrt(%s) =' % a, cube_root(a))
     """)

node("c_for", "concept", "for 迴圈", 3, parent="ch3", en="for loop",
     desc="""
     for [iterating_variable] in [sequence]:
         statements
     迴圈次數確定 (走訪序列) 時通常使用 for。""",
     uses=["c_membership"], related=["c_while"],
     code="""
     ## (1) 輸出字串中的字母
     i = 0
     for alpha in 'Python 3.11.1':
         i = i + 1
         print(' 第 ', i, ' 個字母 :', alpha)

     ## (2) 輸出串列中的元素
     languages = ['English', 'Python', 'Assembly']
     for language in languages:
         print(' Language Version :', language)

     ## (3) 計算字串長度
     for count in languages:
         print(count, '\\t length =', len(count))
     """)

node("q3_for_zh", "exercise", "練習：for 迴圈處理中文字串", 3, parent="c_for",
     practice=["c_for"],
     desc="修改 Example 3.1：(1) 輸出中文字串中的文字 (2) 輸出串列 ['齊天大聖', '孫悟空', '花果山水簾洞'] 中的元素 (3) 計算各字串長度。",
     code="""
     for i, ch in enumerate('第十個字母是六', start=1):
         print('第', i, '個字 :', ch)

     names = ['齊天大聖', '孫悟空', '花果山水簾洞']
     for name in names:
         print(name, '\\t length =', len(name))
     """)

node("c_break", "concept", "break / continue / pass / for-else", 3, parent="c_for",
     desc="""
     continue：進入下一次迭代。
     break   ：離開迴圈。
     pass    ：什麼都不做 (語法佔位)。
     for ... else：迴圈「沒有被 break」正常結束時才執行 else 區塊。""",
     refs=["https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops"],
     code="""
     for n in range(10):
         if n % 2 == 0:
             continue      # 跳過偶數
         if n > 7:
             break         # 離開迴圈
         print(n, end=' ') # 1 3 5 7
     print()
     for n in range(3):
         pass              # 佔位，不做事
     else:
         print('loop finished without break')
     """)

node("c_membership", "concept", "成員運算子 in / not in", 3, parent="c_for",
     en="Membership operators",
     desc="in：值在序列 / 集合中則為 True；not in 則相反。"
          "優先權與比較運算子相同。對 set / dict 的成員測試速度遠快於 list。",
     related=["c_compare"],
     code="""
     A = []
     for x in [1, 2, 5, 10]:
         if x not in [x*2, 10-x]:
             A.append(x)
     print(A)                   # [1, 2, 10]
     print('Py' in 'Python')    # True
     """)

node("ex_insert_copy", "example", "Example 3.2 迴圈中複製並插入元素", 3, parent="c_for",
     desc="迴圈中要修改正在走訪的串列時，應走訪它的切片複本 fruits[:]，否則可能無窮迴圈。",
     uses=["c_for", "c_slicing", "c_list_methods"],
     code="""
     fruits = ['apple', 'mango', 'watermelon', 'banana', 'pineapple']
     print('fruits (before) =', fruits)
     for f in fruits[:]:            # 走訪整個串列的切片複本
         if len(f) <= 8 and len(f) >= 5:
             fruits.insert(4, f)
     print('fruits (after) =', fruits)
     # ['apple', 'mango', 'watermelon', 'banana', 'banana', 'mango', 'apple', 'pineapple']
     """)

node("q3_insert", "exercise", "練習：插入位置與 or 條件", 3, parent="c_for",
     practice=["ex_insert_copy"],
     desc="(1) 插入至原來 banana 與 pineapple 之間 (2) 複製條件改為 len(f) <= 6 或 > 9。",
     code="""
     fruits = ['apple', 'mango', 'watermelon', 'banana', 'pineapple']
     pos = fruits.index('pineapple')        # banana 與 pineapple 之間
     for f in fruits[:]:
         if len(f) <= 6 or len(f) > 9:
             fruits.insert(pos, f)
             pos += 1                       # 保持原插入順序
     print(fruits)
     """)

node("f_range", "function", "range()", 3, parent="c_for",
     en="range(start, stop, step)",
     desc="產生整數序列：包含 start、不包含 stop；預設 start=0, step=1。"
          "range 是內建的序列型別之一 (list, tuple, range)。",
     related=["c_slicing", "c_sequence"],
     code="""
     for i in range(2, 10):
         print(i, end=' ')          # 2 3 4 5 6 7 8 9
     print()
     print(range(5))                # range(0, 5)
     print(list(range(5)))          # [0, 1, 2, 3, 4]
     print(tuple(range(5)))         # (0, 1, 2, 3, 4)
     print(list(range(-15, 25, 3)))
     print(list(range(-15, -25, -3)))
     """)

node("ex_range_for", "example", "Example 3.3 range() 與 for", 3, parent="c_for",
     uses=["f_range", "f_len"],
     desc="以 range 累加、以 range(len(seq)) 取索引，以及巢狀迴圈。",
     code="""
     s, n = 0, 5
     for i in range(n):
         s = s + i
         print(i, end='')
         if i < (n-1): print(end=' + ')
     print(' = ', s)
     print('sum(range(5)) = ', sum(range(5)))

     notes = ['ti', 'do', 're', 'mi', 'fa', 'sol', 'la']
     for i in range(len(notes)):
         print('notes[', i, '] : ', notes[i])

     # 巢狀迴圈 (Nested Loop)
     for i in range(10):
         for j in range(10):
             print((j+i) % 10, end='')
         print()
     """)

node("ex_prime1", "example", "範例：搜尋小於 100 的質數 (解法一 in / not in)", 3,
     parent="c_for", uses=["c_membership", "f_range", "c_list_methods"],
     tags=["演算法", "質數"],
     desc="先找出所有合成數 (2~10 的倍數)，再排除合成數得到質數。",
     code="""
     prime_numbers = []
     composite_numbers = []
     for i in range(2, 11):
         for j in range(i*2, 100, i):
             composite_numbers.append(j)
     for x in range(2, 100):
         if x not in composite_numbers:
             prime_numbers.append(x)
     print('Prime Numbers (< 100) : ', prime_numbers)
     """)

node("ex_prime2", "example", "範例：搜尋質數 (解法二 for-else + break)", 3,
     parent="c_for", uses=["c_break", "f_range"], related=["ex_prime1"],
     tags=["演算法", "質數"],
     code="""
     prime = []
     for n in range(2, 100):
         for x in range(2, n):
             if n % x == 0:
                 break
         else:
             # loop fell through without finding a factor
             prime.append(n)
             continue
         print('{:2d}'.format(n), end=' ')   # 合成數
     print('\\n are composite numbers less than 100.')
     print('Prime Numbers (< 100) : ', prime)
     """)

node("ex_bubble", "example", "範例：氣泡排序 Bubble Sort", 3, parent="c_for",
     uses=["c_for", "f_range", "c_indexing"], tags=["演算法", "排序"],
     desc="相鄰兩元素比較，順序錯誤就交換；重複 n 輪後由小排到大。",
     code="""
     fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
     print('尚未排序的資料：\\n', fruits)
     for j in fruits:
         for i in range(len(fruits)-1):
             if fruits[i] > fruits[i+1]:
                 temp = fruits[i]          # Swapping
                 fruits[i] = fruits[i+1]
                 fruits[i+1] = temp
     print('由小排到大的資料：\\n', fruits)
     """)

node("q3_bubble_desc", "exercise", "練習：氣泡排序由大排到小", 3, parent="c_for",
     practice=["ex_bubble"],
     code="""
     fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
     for _ in fruits:
         for i in range(len(fruits)-1):
             if fruits[i] < fruits[i+1]:          # 只需把 > 改成 <
                 fruits[i], fruits[i+1] = fruits[i+1], fruits[i]
     print('由大排到小的資料：', fruits)
     """)

node("ex_lotto", "example", "範例：樂透彩隨機選號", 3, parent="c_for",
     uses=["c_while", "c_for", "c_list_methods"], tags=["亂數"],
     desc="從 1~49 中以系統時間為亂數種子隨機選出 6 個不重複號碼；"
          "選中的號碼從候選串列中移除。",
     stdin=["n"],
     code="""
     from random import random
     min_num, max_num, six_num = 1, 49, 6

     yorn = 'y'
     while yorn == 'y' or yorn == 'Y':
         max_dim = max_num - min_num + 1
         lotto = []
         for i in range(max_dim):
             lotto.append(min_num + i)

         select = []
         for i in range(six_num):
             random_num = random() * 10000
             lotto_num = int(random_num % max_dim)
             select.append(lotto[lotto_num])
             for j in range(lotto_num, max_dim-1):
                 lotto[j] = lotto[j+1]          # 移除已經選中的號碼
             max_dim -= 1

         print("\\n 本期樂透彩 電腦選號 如下：(1 ~ 49)")
         for i in range(six_num):
             print(select[i], end='\\t')
         yorn = input("\\n 是否繼續 電腦選號？(y/n)：")
     """)

node("q3_1", "exercise", "Exercise 3.1 遞減數字三角形", 3, parent="ch3",
     practice=["c_for", "c_while"],
     desc="輸出 123456789、12345678 … 1。",
     code="""
     # for 版本
     for n in range(9, 0, -1):
         for k in range(1, n + 1):
             print(k, end='')
         print()

     # while 版本
     n = 9
     while n > 0:
         print(''.join(str(k) for k in range(1, n + 1)))
         n -= 1
     """)

node("q3_2", "exercise", "Exercise 3.2 遞增數字三角形", 3, parent="ch3",
     practice=["c_for", "c_while"],
     desc="輸出 1、12、123 … 123456789。",
     code="""
     for n in range(1, 10):
         for k in range(1, n + 1):
             print(k, end='')
         print()

     n = 1
     while n <= 9:
         print(''.join(str(k) for k in range(1, n + 1)))
         n += 1
     """)

node("q3_3", "exercise", "Exercise 3.3 大寫字母循環排列", 3, parent="ch3",
     practice=["ex_range_for"], uses=["c_slicing"],
     desc="ABCDEFGHIJ / BCDEFGHIJA / … / JABCDEFGHI",
     code="""
     letters = 'ABCDEFGHIJ'
     for i in range(10):
         for j in range(10):
             print(letters[(i + j) % 10], end='')
         print()

     # 另解：切片
     for i in range(10):
         print(letters[i:] + letters[:i])
     """)

node("q3_4", "exercise", "Exercise 3.4 小於 1000 且與 45 互質的自然數", 3,
     parent="ch3", practice=["ex_gcd"], uses=["c_for"],
     code="""
     def gcd(a, b):
         while a != 0:
             a, b = b % a, a
         return b

     coprimes = []
     for n in range(1, 1000):
         if gcd(n, 45) == 1:
             coprimes.append(n)
     print(coprimes)
     print('個數 =', len(coprimes))     # 533
     """)

node("q3_6", "exercise", "Exercise 3.6 樂透選號 + 氣泡排序", 3, parent="ch3",
     practice=["ex_lotto", "ex_bubble"],
     desc="隨機產生 6 個 1~49 的樂透號碼，再以氣泡排序由小到大排序。",
     code="""
     from random import random

     def lotto_pick(k=6, lo=1, hi=49):
         pool = list(range(lo, hi + 1))
         picks = []
         for _ in range(k):
             idx = int(random() * 10000) % len(pool)
             picks.append(pool.pop(idx))     # 取出並移除
         return picks

     def bubble_sort(a):
         a = a[:]
         for _ in range(len(a)):
             for i in range(len(a) - 1):
                 if a[i] > a[i + 1]:
                     a[i], a[i + 1] = a[i + 1], a[i]
         return a

     nums = lotto_pick()
     print('電腦選號 :', nums)
     print('排序後   :', bubble_sort(nums))
     """)

# ============================================================================
# Ch04 資料結構一：序列資料型別
# ============================================================================
node("ch4", "chapter", "Ch04 序列資料型別 list / tuple / str", 4, parent="root",
     en="Data Structure I — Sequence Datatypes",
     desc="內建序列：list、tuple、range，以及文字序列 str、二進位序列 bytes。",
     refs=["https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range"],
     prereq=["ch3"])

node("c_sequence", "concept", "序列資料型別", 4, parent="ch4",
     en="Sequence types",
     desc="有順序、可用索引存取的資料型別：list (可變)、tuple (不可變)、range、"
          "str (文字)、bytes (二進位)。",
     related=["c_immutable", "c_nonsequence"])

node("c_seq_ops", "concept", "4.1 基本序列運算 in / * / [] / +", 4, parent="c_sequence",
     en="Common sequence operations",
     desc="x in s、s * n (重複)、s[i] / s[i:j:k] (索引切片)、s1 + s2 (串接)。",
     uses=["c_membership", "c_indexing", "c_slicing", "c_str_concat"],
     code="""
     seq = []
     for i in range(10):
         seq.append(i**2)
     print(seq)            # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
     print(seq[3])         # 9
     print(seq[3:8])       # [9, 16, 25, 36, 49]
     print(seq[3:8:3])     # [9, 36]
     print([0] + seq[:3])  # 串接
     print(seq * -1)       # [] 乘以負數得到空序列
     """)

node("ex_repeat_alias", "example", "Example 4.1 seq * n 的共用參照陷阱", 4,
     parent="c_seq_ops", uses=["c_seq_ops", "c_alias"], tags=["陷阱"],
     desc="[[]] * 4 會產生「4 個指向同一個 list 的參照」，修改其中一個，全部都會變。"
          "用 append 或 list comprehension 才能建立獨立的子串列。",
     code="""
     list1 = [[1]]
     list2 = list1 * 2
     list2[0].append(2)
     print(list2)            # [[1, 2], [1, 2]]  兩個元素是同一個物件!

     list1 = []
     for i in range(4):
         list1.append([])    # 4 個不同的空串列
     list2 = [[]] * 4        # 4 個參照指向同一個空串列

     def list_elements(list0):
         for i in range(len(list0)):
             list0[i].append(2*i)
         return list0

     print('list1 (after) = ', list_elements(list1))  # [[0], [2], [4], [6]]
     print('list2 (after) = ', list_elements(list2))  # [[0, 2, 4, 6]] * 4
     """)

node("c_list", "concept", "4.2 list 串列 (可變序列)", 4, parent="ch4",
     en="list — mutable sequence",
     desc="可儲存不同型別的資料。產生方式：[]、[10, True, 'c']、list()、list(iterable)。",
     related=["c_sequence", "c_immutable"], tags=["資料結構"])

node("c_list_methods", "function", "list 方法", 4, parent="c_list",
     en="append / extend / insert / remove / pop / index / count / sort / copy / del",
     desc="""
     append(x)      在尾端加入一個元素
     extend(it)     把可迭代物件的元素逐一加入 (= lst[len(lst):] = it)
     insert(i, x)   在索引 i 插入 x
     remove(x)      移除第一個 x (不存在 → ValueError)
     pop([i])       移除並回傳索引 i (預設最後一個)
     index(x)       回傳 x 的索引 (不存在 → ValueError)
     count(x)       計算 x 出現次數
     sort()         就地排序
     copy()         淺複製 (= lst[:])
     del lst[i]     刪除元素""",
     code="""
     words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
     print(words.index('up'))       # 4
     print(words.count('fly'))      # 1
     w = []
     w.extend(words[0:3])           # ['Fly', 'robin', 'fly']
     words.insert(3, w); print(words)
     words.remove(w);    print(words)
     words.insert(3, 'Fly')
     del words[3]
     words.sort();       print(words)  # 大寫字母排在小寫之前
     print(words.pop())             # 'up'
     print(words.pop(3))            # 'robin'
     print(words)

     a = ['A', 'b', 'C']
     b = a.copy(); c = a.copy()
     b.append([1.41, 3.14])         # 加入「一個」元素 (巢狀串列)
     c.extend([1.41, 3.14])         # 逐一加入元素
     print(b, c)
     """)

node("c_alias", "concept", "參照 (alias) vs 複製 (copy)", 4, parent="c_list",
     en="Aliasing vs copying",
     desc="list0 = listNumbers 只是讓兩個名稱指向同一個物件 (local symbol table 重新命名)，"
          "修改其一另一個也會變。用 extend()、copy() 或 [:] 產生複本。",
     related=["c_variable", "c_immutable"], tags=["陷阱", "核心觀念"],
     code="""
     listNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
     list0 = listNumbers           # alias: 同一個物件
     list0.append('a')
     print(listNumbers)            # 也多了 'a' !

     listNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
     list1 = []
     list1.extend(listNumbers)     # Method 1 : extend()
     list2 = listNumbers.copy()    # Method 2 : copy()
     list3 = listNumbers[:]        # Method 3 : slicing
     list1.append('A'); list2.append(2020); list3.append(None)
     print(listNumbers)            # 不變
     print(list0 is listNumbers, list2 is listNumbers)
     """)

node("ex_stack", "example", "Example 4.2-4 用 list 實作 Stack 堆疊 (LIFO)", 4,
     parent="c_list", uses=["c_list_methods", "c_while"],
     tags=["資料結構", "Stack"],
     desc="Stack 後進先出 (Last-In-First-Out)。push = append()、pop = pop()。"
          "相關操作：top、IsEmpty、IsFull、getSize。",
     stdin=["a", "b", "c", "d", "null"],
     code="""
     def Stack(prompt=' Push to Stack (type null if done): '):
         stack = []
         while True:
             top = input(prompt)
             if top in ('n', 'nu', 'nul', 'null'):
                 break
             else:
                 stack.append(top)               # push

         print('\\n Within Stack: ', stack)
         print(' <<< Pop the Stack --> LIFO : Last-In-First-Out ')
         for _ in range(len(stack)):
             print(' pop Stack : ', stack.pop())  # pop
         print(' ******* Stack = ', stack)

     Stack()
     """)

node("q4_2", "exercise", "Exercise 4.2 用 list 實作 Queue 佇列 (FIFO)", 4,
     parent="c_list", practice=["ex_stack"], uses=["c_list_methods"],
     tags=["資料結構", "Queue"],
     desc="Queue 先進先出 (First-In-First-Out)：enqueue = append()、dequeue = pop(0)。"
          "(大量資料時建議改用 collections.deque 的 popleft())",
     stdin=["a", "b", "c", "null"],
     code="""
     def Queue(prompt=' Enqueue (type null if done): '):
         queue = []
         while True:
             item = input(prompt)
             if item in ('n', 'nu', 'nul', 'null'):
                 break
             queue.append(item)                     # enqueue
         print('\\n Within Queue: ', queue)
         print(' >>> Dequeue --> FIFO : First-In-First-Out ')
         while queue:                               # 非空串列為 True
             print(' dequeue : ', queue.pop(0))     # dequeue
         print(' ******* Queue = ', queue)

     Queue()
     """)

node("c_list_comp", "concept", "List Comprehension 串列精簡", 4, parent="c_list",
     en="List comprehension",
     desc="仿照數學集合寫法產生串列：[運算式 for 變數 in 可迭代 if 條件]。"
          "A = {2n+1 | n=1..9} → [2*n+1 for n in range(1,10)]。通常比 for + append 更快。",
     uses=["c_for", "f_range"], tags=["Comprehension"],
     code="""
     A = [2*n+1 for n in range(1, 10)]
     B = [x**2 for x in A if x < 12]
     print('A = ', A)   # [3, 5, 7, 9, 11, 13, 15, 17, 19]
     print('B = ', B)   # [9, 25, 49, 81, 121]

     # 巢狀迴圈 → 一行
     pairs = [(i, j) for i in ['Apple', 'Android', 'Asus']
                     for j in ['Google', 'Apple', 'Microsoft'] if i != j]
     print(pairs)
     """)

node("ex_listcomp_math", "example", "Example 4.2-7 List Comprehension on Math", 4,
     parent="c_list_comp", uses=["c_list_comp"],
     code="""
     from math import exp, pi
     print([str(round(exp(1), i)) for i in range(1, 6)])
     # ['2.7', '2.72', '2.718', '2.7183', '2.71828']
     print([float(round(pi*10**2, i)) for i in range(1, 6)])
     # [314.2, 314.16, 314.159, 314.1593, 314.15927]
     """)

node("ex_prime_listcomp", "example", "Example 4.2-8 以 List Comprehension 找質數", 4,
     parent="c_list_comp", uses=["c_list_comp", "c_membership"],
     refactors=["ex_prime1"], tags=["質數"],
     code="""
     composite_numbers = [j for i in range(2, 11) for j in range(i*2, 100, i)]
     prime_numbers = [x for x in range(2, 100) if x not in composite_numbers]
     print('Prime Numbers (< 100) : ', prime_numbers)

     # 再精簡成一個運算式
     prime_numbers = [x for x in range(2, 100)
                      if x not in [j for i in range(2, 11)
                                   for j in range(i*2, 100, i)]]
     print(prime_numbers)
     """)

node("q4_1", "exercise", "Exercise 4.1 list 方法組合", 4, parent="c_list",
     practice=["c_list_methods"],
     desc="以 w = ['Fly','robin','fly'] 與 words 運算出 "
          "['Fly','robin','fly','Fly','robin','fly','Fly','robin','fly','Up','up','to','the','sky']。",
     code="""
     w = ['Fly', 'robin', 'fly']
     words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
     words[3:3] = w * 2          # 在索引 3 插入兩份 w (切片指定)
     print(words)

     # 另解：用 insert 逐一插入
     words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
     for k, x in enumerate(w * 2):
         words.insert(3 + k, x)
     print(words)
     """)

node("q4_3", "exercise", "Exercise 4.3 以 list comprehension 改寫 pairs", 4,
     parent="c_list_comp", practice=["c_list_comp"],
     code="""
     pairs = [(i, j, (i + j) / 2) for i in [1, 3, 5] for j in [4, 1, 2] if i != j]
     print(pairs)
     """)

node("q4_4", "exercise", "Exercise 4.4 輸入 N，找出小於 N 的質數", 4,
     parent="c_list_comp", practice=["ex_prime_listcomp"], stdin=["50"],
     desc="(1) 一般迴圈寫法 (2) list comprehension 寫法。",
     code="""
     N = int(input('N = '))

     # (1) for 迴圈 + for-else
     primes = []
     for n in range(2, N):
         for x in range(2, int(n ** 0.5) + 1):
             if n % x == 0:
                 break
         else:
             primes.append(n)
     print(primes)

     # (2) list comprehension
     primes = [n for n in range(2, N)
               if all(n % x for x in range(2, int(n ** 0.5) + 1))]
     print(primes)
     """)

node("c_tuple", "concept", "4.3 tuple 元組 (不可變序列)", 4, parent="ch4",
     en="tuple — immutable sequence",
     desc="""
     tuple 由「逗號」產生，小括號通常只是選項：
       ()            空 tuple
       a,  或 (a,)    單一元素 tuple (注意 t = 'Python' 只是字串)
       a, b, c       一般 tuple
       tuple(iterable)
     tuple 不可修改元素 (TypeError)，但元素本身可以是可變物件 (例如 list)。
     常用來儲存異質資料。""",
     related=["c_immutable", "c_sequence"], tags=["資料結構"],
     code="""
     t = ();                   print(t)
     t = 'Python',;            print(t)        # ('Python',)
     t = 'Python', 123, 3.1416;print(t)
     t1 = ('ABC', 'NBC', 'CBS'), t, (2.71828, 1.732)   # nested tuple
     print(t1)
     t2 = ['a', 'b', 'c', 1, 2], [11, 22], ('Python', 3.6)
     t2[0].append(3)           # 元素是 list → 可修改 list 本身
     print(t2)
     try:
         t2[0] = [97, 98, 99]
     except TypeError as e:
         print('TypeError:', e)
     """)

node("c_tuple_unpacking", "concept", "tuple packing / unpacking 與交換", 4,
     parent="c_tuple", en="Packing & unpacking",
     desc="t = 1, 2, 3 為 packing；a, b, c = t 為 unpacking。"
          "a, b = b, a+b 這類寫法就是先 pack 再 unpack，可一行完成交換 (swap)。",
     code="""
     t1 = (('ABC', 'NBC', 'CBS'), ('Python', 123, 3.1416), (2.71828, 1.732))
     tv, py, math = t1
     print(tv); print(py); print(math)
     a, b = 1, 2
     a, b = b, a        # swap
     print(a, b)
     """)

node("f_enumerate", "function", "enumerate()", 4, parent="c_tuple",
     en="enumerate(iterable, start=0)",
     desc="回傳 (索引, 元素) tuple 的迭代器。",
     refs=["https://docs.python.org/3/library/functions.html#enumerate"],
     code="""
     languages = ['Python', 'R', 'Scala']
     print(list(enumerate(languages)))           # [(0, 'Python'), ...]
     print(list(enumerate(languages, start=1)))
     for index, element in enumerate(languages, start=1):
         print(index, element)
     """)

node("f_zip", "function", "zip()", 4, parent="c_tuple", en="zip(*iterables)",
     desc="把多個序列「拉鍊式」配對成 tuple 的迭代器，可同時走訪兩筆序列。",
     refs=["https://docs.python.org/3/library/functions.html#zip"],
     code="""
     positions = ['Pitcher', 'Shortstop', 'Third Baseman']
     players = ['Chien-Ming Wang', 'Derek Jeter', 'A. Rod']
     for pos, player in zip(positions, players):
         print('Who is the {0}? It is {1}.'.format(pos, player))
     """)

node("f_tuple", "function", "tuple() 建構子", 4, parent="c_tuple",
     desc="tuple(iterable) 只接受 1 個參數；字串會被拆成字元。"
          "tuple(t1[1:2]) 得到 ((…),)，tuple(t1[1]) 得到內層 tuple 本身。",
     code="""
     print(tuple())                    # ()
     print(tuple(range(2, 7)))         # (2, 3, 4, 5, 6)
     print(tuple('abc'))               # ('a', 'b', 'c')
     print(tuple(['a', 'b', 'c']))
     t1 = (('ABC', 'NBC', 'CBS'), ('Python', 123, 3.1416), (2.71828, 1.732))
     print(tuple(t1[1:2]))             # (('Python', 123, 3.1416),)
     print(tuple(t1[1]))               # ('Python', 123, 3.1416)
     # tuple('a', 'b', 'c')  # TypeError: tuple expected at most 1 argument
     """)

node("ex_tuple_algos", "example", "Example 4.3 以 tuple 交換改寫 Fibonacci / GCD / 氣泡排序", 4,
     parent="c_tuple", uses=["c_tuple_unpacking"],
     refactors=["ex_fib", "ex_gcd", "ex_bubble"],
     code="""
     # 費氏數列 (< 1000)
     a, b = 0, 1
     while b < 1000:
         print(b, end=' ')
         a, b = b, a+b              # (a, b) = (b, a+b)
     print()

     # GCD
     a, b = 21, 144
     while a != 0:
         a, b = b % a, a            # (a, b) = (b % a, a)
     print('GCD =', b)

     # 氣泡排序
     fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
     for _ in fruits:
         for i in range(len(fruits)-1):
             if fruits[i] > fruits[i+1]:
                 fruits[i], fruits[i+1] = fruits[i+1], fruits[i]
     print(fruits)
     """)

node("c_str_methods", "function", "4.4 str 字串方法", 4, parent="ch4",
     en="str methods",
     desc="""
     str 是以 Unicode 編碼的不可變序列。常用方法：
     capitalize() casefold() center(w) count(sub) encode() find(sub) index(sub)
     format() join(it) lower() upper() strip() rstrip() replace(old,new)
     split(sep) splitlines()""",
     refs=["https://docs.python.org/3/library/stdtypes.html#textseq"],
     related=["c_str", "c_sequence"], tags=["字串"],
     code="""
     s = '  Hello Python  '
     print(s.strip(), '|', s.upper(), '|', s.lower())
     print('python'.capitalize(), 'Python'.center(12, '*'))
     print('banana'.count('a'), 'banana'.find('n'), 'banana'.replace('a', 'A'))
     print('-'.join(['2024', '03', '01']))
     print('a,b,,c'.split(','))
     print('{0} is {1} years old'.format('Alice', 20))
     print('Ünïcode'.encode('utf-8'))
     """)

node("ex_str_split", "example", "Example 4.4 split() / splitlines() 斷字", 4,
     parent="c_str_methods", uses=["c_str_methods", "c_for"],
     code='''
     string = """Towers of gold are still too little
     These hands could hold the world but it'll
     Never be enough
     Never be enough
     For me"""
     print(string.lower())
     print(string.split(sep=' '))      # 換行字元會黏在單字上
     print(string.split(sep='\\n'))
     string_lines = string.splitlines()
     string1 = []
     for line in string_lines:
         string1.append(line.split(sep=' '))
     print(string1)
     ''')

node("q4_5", "exercise", "Exercise 4.5 字數統計 Word Counts (Never Enough)", 4,
     parent="c_str_methods", practice=["ex_str_split"],
     uses=["c_str_methods", "c_list_comp", "c_list_methods"], tags=["Word Count"],
     desc="""
     將歌詞斷字並計算每個單字的出現次數，排序後左右對齊輸出。
     A. 大小寫視為不同單字 (Never ≠ never)
     B. 以空白分割
     C. 移除單字結尾的標點符號 (? , . !)
     D. 字首或字內的縮寫符號 ('Cause、it'll) 保留""",
     code='''
     lyrics = """I'm trying to hold my breath
     Let it stay this way
     Can't let this moment end
     You set off a dream with me
     Getting louder now
     Can you hear it echoing?
     Take my hand
     Will you share this with me?
     'Cause darling without you
     All the shine of a thousand spotlights
     All the stars we steal from the nightsky
     Will never be enough
     Never be enough
     Towers of gold are still too little
     These hands could hold the world but it'll
     Never be enough
     Never be enough
     For me
     Never, never
     Never, never
     Never, for me
     Never enough
     Never enough
     Never enough
     For me
     For me
     For me
     For me"""

     # (1) 一般寫法
     words = []
     for w in lyrics.split():
         words.append(w.rstrip('?,.!'))
     counts = []
     for k in sorted(set(words)):
         counts.append((k, words.count(k)))
     for k, c in counts:
         print('{0:12s}{1:3d}'.format(k, c))

     # (2) List Comprehension 精簡版
     words = [w.rstrip('?,.!') for w in lyrics.split()]
     print('\\n'.join('{0:12s}{1:3d}'.format(k, words.count(k)) for k in sorted(set(words))))
     ''')

node("c_bytes4", "concept", "4.5 bytes 物件", 4, parent="ch4",
     desc="bytes 是由單一位元組組成的不可變序列，與 ASCII 相容。"
          "class bytes([source[, encoding[, errors]]])",
     refs=["https://docs.python.org/3/library/stdtypes.html#binaryseq"],
     related=["c_bytes"])

# ============================================================================
# Ch05 資料結構二：set / frozenset / dict
# ============================================================================
node("ch5", "chapter", "Ch05 set / frozenset / dict", 5, parent="root",
     en="Data Structure II — set, frozenset, dictionary",
     desc="三種內建非序列資料型別：set (可變)、frozenset (不可變)、dict (可變映射)。",
     prereq=["ch4"])

node("c_nonsequence", "concept", "非序列資料型別", 5, parent="ch5",
     en="Nonsequence types",
     desc="元素沒有索引順序 (set) 或以 key 存取 (dict)；以雜湊 (hash) 實作，成員測試很快。",
     related=["c_immutable"])

node("c_set", "concept", "5.1 set 集合 (可變)", 5, parent="ch5", en="set",
     desc="""
     元素不重複、不保留順序 (unordered)。用途：成員測試、去除重複、集合數學運算。
     產生方式：{1, 2, 3} 或 set(iterable)。
     空集合一定要用 set()；{} 是空字典！""",
     refs=["https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset"],
     related=["c_nonsequence", "c_membership"], tags=["資料結構"],
     code="""
     words = {'Hello', 'world', 'hello', 'Python', 'hello', 'sets'}
     print(words)                 # 去除重複 + 不依次序
     print('sets' in words)       # True  成員測試
     print('Sets' in words)       # False
     print(set('Python'))         # 字串拆成字元集合
     print({'Python'})            # 只有一個元素的集合
     print(type({}), type(set()))
     """)

node("c_set_methods", "function", "set 方法 add / remove / discard / pop / clear", 5,
     parent="c_set",
     desc="remove(x) 在 x 不存在時產生 KeyError；discard(x) 則不會。"
          "pop() 移除並回傳「任意」元素。",
     code="""
     words = set()
     words.add(1);                 print(words)   # {1}
     words = set([1, 2, 2, 3, 4, 5]); print(words) # {1, 2, 3, 4, 5}
     words.remove(2);              print(words)
     try:
         words.remove(2)
     except KeyError as e:
         print('KeyError:', e)
     words.discard(2)              # 不存在也不會出錯
     print(words.pop())            # 任意一個元素
     words.clear();                print(words)   # set()
     """)

node("c_set_compare", "concept", "集合比較：子集合 / 超集合", 5, parent="c_set",
     desc="== != ；< 真子集合、<= 子集合、> 真超集合、>= 超集合。",
     uses=["c_compare"],
     code="""
     set1 = {1, 2, 3, 4}
     set2 = {1, 2, 3, 4, 5, 6}
     print(set1 == set2, set1 != set2)   # False True
     print(set1 > set2, set1 >= set2)    # False False
     print(set1 < set2, set1 <= set2)    # True True
     """)

node("c_set_ops", "concept", "集合運算 & | - ^", 5, parent="c_set",
     en="intersection / union / difference / symmetric difference",
     desc="""
     &  交集 intersection
     |  聯集 union
     -  差集 difference
     ^  對稱差集 symmetric difference (XOR)
        A ⊕ B = (A ∪ B) − (A ∩ B) = (A − B) ∪ (B − A)""",
     code="""
     word_py1 = set('Python')
     word_py2 = set('Pythagoras')
     print(word_py2 & word_py1)   # {'P','h','o','t','y'}
     print(word_py2 | word_py1)   # 聯集
     print(word_py2 - word_py1)   # {'a','g','r','s'}
     print(word_py1 - word_py2)   # {'n'}
     print(word_py2 ^ word_py1)   # {'a','g','n','r','s'}
     """)

node("c_set_comp", "concept", "Set Comprehension", 5, parent="c_set",
     desc="{運算式 for x in 可迭代 if 條件} 產生集合。",
     related=["c_list_comp"], tags=["Comprehension"],
     code="""
     word_py1 = set('Python')
     word_py2 = set('Pythagoras')
     print({x for x in word_py2 if x in word_py1})       # intersection
     print({x for x in word_py2 if x not in word_py1})   # word_py2 - word_py1
     print({x for x in word_py1 if x not in word_py2})   # word_py1 - word_py2
     """)

node("ex_set_wc", "example", "Example 5.1-7 以 set 做字數統計", 5, parent="c_set",
     uses=["c_set", "c_list_methods"], tags=["Word Count"],
     desc="set(words) 取得不重複的關鍵字，再用 list.count() 計數。",
     code="""
     words = ['Hello', 'world', 'hello', 'Python', 'list',
              'dictionary', 'tuple', 'hello', 'Hello',
              'set', 'tuple', 'python', 'dictionary', 'set',
              'array', 'binary', 'tuple', 'hello', 'data']
     key_words = set(words)
     word_counts = []
     for i in key_words:
         word_counts.append((i, words.count(i)))
     for w, c in word_counts:
         print('{0:15s} {1:2d}'.format(w, c))
     """)

node("q5_1", "exercise", "Exercise 5.1 以 Set Comprehension 寫聯集與對稱差集", 5,
     parent="c_set", practice=["c_set_comp", "c_set_ops"],
     code="""
     word_py1 = set('Python')
     word_py2 = set('Pythagoras')

     union = {x for s in (word_py1, word_py2) for x in s}
     sym_diff = ({x for x in word_py1 if x not in word_py2} |
                 {x for x in word_py2 if x not in word_py1})
     # 或寫成單一 comprehension：
     sym_diff2 = {x for x in word_py1 | word_py2
                  if (x in word_py1) != (x in word_py2)}

     print(union == word_py1 | word_py2, union)
     print(sym_diff == word_py1 ^ word_py2, sym_diff)
     print(sym_diff2 == sym_diff)
     """)

node("c_frozenset", "concept", "5.2 frozenset (不可變集合)", 5, parent="ch5",
     en="frozenset",
     desc="與 set 唯一差異：不可改變。沒有 add / discard 等方法 (AttributeError)，"
          "但可做比較與集合運算；因為可雜湊，可以當 dict 的 key 或 set 的元素。",
     related=["c_set", "c_immutable"], tags=["資料結構"],
     code="""
     f1 = frozenset([1, 2, 3])
     f2 = frozenset([1, 2, 3, 4, 5])
     print(f1 < f2, f1 > f2)       # True False
     print(f1 & f2, f2 - f1)
     print({x for x in f2 if x not in f1})
     try:
         f1.add(4)
     except AttributeError as e:
         print('AttributeError:', e)
     d = {frozenset({'a', 'b'}): 'ok'}   # 可以當 key
     print(d)
     """)

node("ex_frozen_wc", "example", "Example 5.2 frozenset + list comprehension 字數統計", 5,
     parent="c_frozenset", uses=["c_frozenset", "c_list_comp"],
     refactors=["ex_set_wc"], tags=["Word Count"],
     code="""
     words = ['Hello', 'world', 'hello', 'Python', 'list',
              'dictionary', 'tuple', 'hello', 'Hello',
              'set', 'tuple', 'python', 'dictionary', 'set',
              'array', 'binary', 'tuple', 'hello', 'data']
     kw = frozenset(words)
     word_counts = [(i, words.count(i)) for i in kw]
     for w, c in word_counts:
         print('{0:15s} {1:2d}'.format(w, c))
     """)

node("c_dict", "concept", "5.3 dict 字典 (可變映射)", 5, parent="ch5",
     en="dict — mapping type",
     desc="""
     不依次序儲存的鍵值對 (key-value pairs)。key 必須是不可變型別
     (數值、字串、元素皆不可變的 tuple)。
     list(d.keys())   取得 key 串列
     sorted(d.keys()) 取得排序後的 key
     key in d         檢查 key 是否存在""",
     refs=["https://docs.python.org/3/library/stdtypes.html#mapping-types-dict"],
     related=["c_nonsequence", "c_immutable"], tags=["資料結構"])

node("c_dict_create", "concept", "dict 的 5 種產生方式", 5, parent="c_dict",
     uses=["f_zip"],
     code="""
     gpa0 = {'C': 2.0, 'B': 3.0, 'A': 4.0, 'F': 'Fail'}
     gpa1 = dict(A=4.0, B=3.0, C=2.0, F='Fail')
     gpa2 = dict({'B': 3.0, 'A': 4.0, 'F': 'Fail', 'C': 2.0})
     gpa3 = dict([('F', 'Fail'), ('C', 2.0), ('A', 4.0), ('B', 3.0)])
     gpa4 = dict(zip(['F', 'C', 'B', 'A'], ['Fail', 2.0, 3.0, 4.0]))
     print(gpa0 == gpa1 == gpa2 == gpa3 == gpa4)   # True
     """)

node("c_dict_ops", "function", "dict 運算：keys / values / items / del / 新增", 5,
     parent="c_dict",
     desc="keys() / values() 回傳「檢視物件」(view)，會隨字典變動；"
          "keys view 支援集合運算 (& |)，但 dict 本身不行。"
          "dict 沒有 append()，新增用 d[key] = value。",
     uses=["c_set_ops"],
     code="""
     fastfood = {'Cheeseburger': 50, 'fries': 25, 'Coke': 35, 'coffee': 45}
     items, prices = fastfood.keys(), fastfood.values()
     print(items, prices, sum(prices))
     print(sorted(items), sorted(prices))
     del fastfood['coffee']                 # 刪除
     print(list(items))                     # view 會跟著變
     print(items & {'Hamburger', 'OJ', 'Coke'})   # {'Coke'}
     print(items | {'Hamburger', 'OJ', 'Coke'})
     fastfood['coffee'] = 25                # 新增
     print('coffee' in fastfood, 'OJ' in fastfood)
     for k, v in fastfood.items():          # (key, value) tuple
         print('{0} : {1}'.format(k, v))
     """)

node("c_dict_comp", "concept", "Dictionary Comprehension", 5, parent="c_dict",
     desc="{key運算式: value運算式 for x in 可迭代 if 條件}",
     related=["c_list_comp", "c_set_comp"], tags=["Comprehension"],
     code="""
     q = {}
     for x in range(0, 6):
         q[x] = x**2 + 2*x + 1
     print(q)
     q = {x: x**2 + 2*x + 1 for x in range(0, 6)}
     print(q)   # {0: 1, 1: 4, 2: 9, 3: 16, 4: 25, 5: 36}
     """)

node("q5_log", "exercise", "練習：以 dict comprehension 精簡 log 表", 5,
     parent="c_dict", practice=["c_dict_comp"],
     code="""
     from math import log
     log_x = {x: round(log(x, 10), 4) for x in (1, 2, 3, 5, 10, 50, 100)}
     print(log_x)
     """)

node("ex_dict_wc", "example", "Example 5.3-7 以 dict 做字數統計", 5, parent="c_dict",
     uses=["c_dict", "c_set", "c_str_methods"], refactors=["ex_set_wc"],
     tags=["Word Count"],
     code='''
     string = """Towers of gold are still too little
     These hands could hold the world but it'll
     Never be enough
     Never be enough
     For me"""
     string1 = []
     for line in string.splitlines():
         for w in line.split(sep=' '):
             string1.append(w)
     key_words = set(string1)
     d_counts = {}
     for k in sorted(key_words):
         d_counts[k] = string1.count(k)
     print(" << The sorted word-count result >>")
     print("\\t WORD \\t\\tCount \\n ", "-"*32)
     for k, v in d_counts.items():
         print('\\t {0:15s} {1:2d}'.format(k, v))
     ''')

node("q5_2", "exercise", "Exercise 5.2 樂透 100 組號碼出現次數統計", 5,
     parent="c_dict", practice=["ex_lotto", "ex_tuple_algos"],
     uses=["c_dict"],
     desc="隨機產生 100 組 6 個 1~49 的號碼，排序後統計各號碼出現次數，"
          "以 {號碼: 次數} 存入 dict 並對齊輸出。",
     code="""
     from random import random

     def lotto_pick(k=6, lo=1, hi=49):
         pool = list(range(lo, hi + 1))
         return [pool.pop(int(random() * 10000) % len(pool)) for _ in range(k)]

     def bubble_sort(a):
         a = a[:]
         for _ in range(len(a)):
             for i in range(len(a) - 1):
                 if a[i] > a[i + 1]:
                     a[i], a[i + 1] = a[i + 1], a[i]
         return a

     draws = [bubble_sort(lotto_pick()) for _ in range(100)]
     for d in draws[:5]:
         print(d)
     print('...')
     counts = {n: 0 for n in range(1, 50)}
     for d in draws:
         for n in d:
             counts[n] += 1
     for n, c in counts.items():
         print('{0:>2d} : {1:>3d}'.format(n, c), end='    ' if n % 5 else '\\n')
     print('\\n總數 =', sum(counts.values()))   # 600
     """)

node("q5_3", "exercise", "Exercise 5.3 以 comprehension 精簡 dict 字數統計", 5,
     parent="c_dict", practice=["ex_dict_wc"],
     code='''
     string = """Towers of gold are still too little
     These hands could hold the world but it'll
     Never be enough
     Never be enough
     For me"""
     words = [w for line in string.splitlines() for w in line.split(' ')]
     d_counts = {k: words.count(k) for k in sorted(set(words))}
     print('\\n'.join('\\t {0:15s} {1:2d}'.format(k, v) for k, v in d_counts.items()))
     ''')

node("q5_4", "exercise", "Exercise 5.4 質數存入 dict {index: prime}", 5,
     parent="c_dict", practice=["q4_4", "c_dict_comp"], uses=["f_enumerate"],
     stdin=["50"],
     code="""
     N = int(input('N = '))
     primes = [n for n in range(2, N)
               if all(n % x for x in range(2, int(n ** 0.5) + 1))]
     prime_dict = {i: p for i, p in enumerate(primes)}
     print(prime_dict)
     """)

node("q5_5", "exercise", "Exercise 5.5 字數統計 Revisited (10 行內)", 5,
     parent="c_dict", practice=["q4_5", "ex_dict_wc"],
     uses=["c_list_comp", "c_set", "c_dict_comp"], tags=["Word Count"],
     desc="綜合 list / tuple / set / dict 與 comprehension，在 10 行敘述內完成 Exercise 4.5。",
     code='''
     lyrics = """I'm trying to hold my breath
     Let it stay this way
     Can't let this moment end
     You set off a dream with me
     Getting louder now
     Can you hear it echoing?
     Take my hand
     Will you share this with me?
     'Cause darling without you
     All the shine of a thousand spotlights
     All the stars we steal from the nightsky
     Will never be enough
     Never be enough
     Towers of gold are still too little
     These hands could hold the world but it'll
     Never be enough
     Never be enough
     For me
     Never, never
     Never, never
     Never, for me
     Never enough
     Never enough
     Never enough
     For me
     For me
     For me
     For me"""
     words = [w.rstrip('?,.!') for w in lyrics.split()]               # list
     counts = {k: words.count(k) for k in sorted(set(words))}         # set + dict
     width = max(len(k) for k in counts)
     print('\\n'.join(f'{k:<{width}} {v:>2}' for k, v in counts.items()))  # tuple
     ''')

# ----------------------------------------------------------------------------
# 跨章節關聯
# ----------------------------------------------------------------------------
edge("c_immutable", "c_str", "related")
edge("c_immutable", "c_tuple", "related")
edge("c_immutable", "c_frozenset", "related")
edge("c_immutable", "c_list", "related")
edge("c_immutable", "c_set", "related")
edge("c_immutable", "c_dict", "related")
edge("c_sequence", "c_str", "related")
edge("c_sequence", "c_list", "related")
edge("c_sequence", "c_tuple", "related")
edge("c_sequence", "f_range", "related")
edge("c_list_comp", "c_set_comp", "related")
edge("c_set_comp", "c_dict_comp", "related")
edge("c_str_methods", "c_str", "related")
edge("ex_fib", "ex_golden", "related")
edge("ex_bsearch", "q3_5", "related")
edge("q4_5", "ex_set_wc", "related")
edge("c_dict", "f_enumerate", "related")


def build_graph():
    """回傳可序列化的知識圖譜 dict，並檢查所有邊都指向存在的節點。"""
    ids = {n["id"] for n in NODES}
    seen, edges = set(), []
    for a, b, r in EDGES:
        assert a in ids and b in ids, f"dangling edge {a} -> {b} ({r})"
        if (a, b, r) not in seen:
            seen.add((a, b, r))
            edges.append({"source": a, "target": b, "rel": r})
    return {
        "meta": {
            "title": "Python 程式設計 知識圖譜 (PyML Ch01–Ch05)",
            "source": "C. Alex Hu, PhD — PyML Ch01–Ch05 講義",
            "kinds": {
                "root": "根", "chapter": "章", "section": "節",
                "concept": "觀念", "function": "函式 / 方法",
                "example": "範例", "exercise": "習題",
            },
            "relations": {
                "contains": "包含", "uses": "使用", "related": "相關",
                "refactors": "改寫自", "practice": "練習", "prereq": "前置",
            },
        },
        "nodes": NODES,
        "edges": edges,
    }
