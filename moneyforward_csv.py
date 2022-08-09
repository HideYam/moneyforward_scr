# import module
import pandas as pd
import glob
import os
import openpyxl
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()
download_path = os.environ['download_path']

# ディレクトリ変更
os.chdir(download_path)

# 空のDataFrameを定義
df = pd.DataFrame()

# .csvを含むファイルをpd.read_csv()で読み込む
firstLoop = True
for i in glob.glob("*.csv*"):
    # header=0 ヘッダーあり
    tmp_df = pd.read_csv(i, encoding="shift-jis")
    #ヘッダー行除外 1回目だけはヘッダーあり、２回目以降は削除
    print(i)
    #if firstLoop:
    #    firstLoop = False
        #df.columns=tmp_df[:0]
    #else:
    #    tmp_df = tmp_df[1:]

    # DataFrameを連結する
    df = pd.concat([df, tmp_df])

#EXCEL

print(df)
df.to_excel(download_path + '/output.xlsx', sheet_name='mfdata', index=False, header=True)
