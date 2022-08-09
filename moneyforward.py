from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
import os
from time import sleep
import matplotlib.pyplot as plt
import chromedriver_binary
from dotenv import load_dotenv

# .envファイルの内容を読み込む 変数は環境ファイルへ
load_dotenv()
download_path = os.environ['download_path']
USER = os.environ['USERID_MF']
PASS = os.environ['PASS_MF']

option = Options()                          # オプションを用意
option.add_argument('--incognito')          # シークレットモードの設定を付与

# seleniumでのダウンロード先のフォルダの設定(※必ずフルパス,env読み込み)

option.add_experimental_option("prefs", {"download.default_directory": download_path})

browser = webdriver.Chrome(options=option)   # Chromeを準備(optionでシークレットモードにしている）

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

sleep(3)

#　パスワードを入力
e = browser.find_element(By.NAME,"mfid_user[password]")
e.clear()
e.send_keys(password)

#　ログインボタンを押す
frm = browser.find_element(By.XPATH,"//form[1]")
frm.submit()

sleep(3)

link = browser.find_element(By.CLASS_NAME,"serviceItem")
link.click()

sleep(3)

frm = browser.find_element(By.XPATH,"//form[1]")
frm.submit()

sleep(10)

#　家計簿アクセスしてダウンロード
link = browser.find_element(By.LINK_TEXT, "家計")
link.click()

sleep(5)

def pagelink():
    page_link = browser.find_element(By.CLASS_NAME, "fc-button-content")
    page_link.click()

def csvdl():
    dl_link = browser.find_element(By.CLASS_NAME, "icon-download-alt")
    dl_link.click()
    sleep(1)
    file_link = browser.find_element(By.LINK_TEXT, "CSVファイル")
    file_link.click()



# p1
csvdl()
sleep(2)

#p2 -
for i in range(2):
    pagelink()
    sleep(5)
    csvdl()
    sleep(2)

# ブラウザを終了
browser.close()
