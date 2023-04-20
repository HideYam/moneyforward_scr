from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import csv
import datetime
import os
from time import sleep
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# .envファイルの内容を読み込む 変数は環境ファイルへ
load_dotenv()
download_path = os.environ['download_path']
USER = os.environ['USERID_MF']
PASS = os.environ['PASS_MF']

option = Options()                          # オプションを用意
option.add_argument('--incognito')          # シークレットモードの設定を付与

# seleniumでのダウンロード先のフォルダの設定(※必ずフルパス,env読み込み)

option.add_experimental_option("prefs", {"download.default_directory": download_path})

# Chromeを準備(optionでシークレットモードにしている）
browser = webdriver.Chrome(ChromeDriverManager().install(),)


### login
url = "https://id.moneyforward.com/sign_in/email"
user_name = USER
password = PASS
browser.get(url)

#メールアドレスを入力
e = browser.find_element(By.NAME,"mfid_user[email]")
e.clear()
e.send_keys(user_name)

#　ログインボタンを押す
frm = browser.find_element(By.XPATH,"//form[1]")
frm.submit()

sleep(2)

#　パスワードを入力
e = browser.find_element(By.NAME,"mfid_user[password]")
e.clear()
e.send_keys(password)

#　ログインボタンを押す
frm = browser.find_element(By.XPATH,"//form[1]")
frm.submit()

sleep(2)

link = browser.find_element(By.CLASS_NAME,"serviceItem")
link.click()

sleep(2)

frm = browser.find_element(By.XPATH,"//form[1]")
frm.submit()

sleep(2)

#　家計簿アクセスしてダウンロード
link = browser.find_element(By.LINK_TEXT, "家計簿")
link.click()

sleep(2)

#pageをめくる
def pagelink():
    page_link = browser.find_element(By.CLASS_NAME, "fc-button-content")
    page_link.click()

def tableget():
    results=[]
    list = browser.find_element(By.CLASS_NAME,"list_body").find_elements(By.TAG_NAME,"tr")

    #西暦取得
    year_match = re.search(r"\d{4}", browser.find_element(By.CLASS_NAME,"fc-header-title.in-out-header-title").text)
    if year_match:
        seireki = year_match.group()  # 検索された数字を取得する
    else:
        print("年を取得できませんでした。")
        sys.exit()

    for i in range(0,len(list)):
        #振替判定　グレーアアウトとかどうか
        if list[i].get_attribute('class') == "transaction_list js-cf-edit-container mf-grayout":
            visible_flag = 0
        else:
            visible_flag = 1

        #tdの中身をループ 順番で処理する
        list_td = list[i].find_elements(By.TAG_NAME,"td")

        hiduke_month, hiduke_day = list_td[1].text.split("/")
        hiduke_day = hiduke_day.split("(")[0]
        hiduke = datetime.date(int(seireki), int(hiduke_month), int(hiduke_day))
        hiduke = hiduke.strftime('%Y/%-m/%-d')

        naiyo = list_td[2].text
        amount = list_td[3].find_element(By.TAG_NAME,"span").text

        card = list_td[4].text.split("\n")[0] #１行目だけにする

        card_detail = list_td[4].get_attribute('data-original-title')

        if "クリックして編集" in card_detail:
            #クリックして編集し、Enterキーを押せば変更出来ます。
            card_detail = ""

        dai = list_td[5].text
        chu = list_td[6].text
        memo = list_td[7].text

        # リストに追加する
        row = [visible_flag, hiduke, naiyo, amount, card, card_detail, dai, chu, memo]
        results.append(row)

    return results

# p1
kakei_data=[]
x=tableget()
kakei_data.append(x)
sleep(2)

#p2 -　rangeでページ数
for i in range(1):
    pagelink()
    sleep(5)
    x=tableget()
    kakei_data.append(x)
    sleep(2)

# CSVファイルに書き込む
current_dir = os.getcwd()
with open(os.path.join(current_dir, 'data.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    for row in kakei_data:
        writer.writerows(row)

# ブラウザを終了
browser.close()
