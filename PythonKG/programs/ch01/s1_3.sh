# 1.3 安裝 Miniconda 與虛擬環境
# 知識點 id: s1_3  |  講義程式

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
