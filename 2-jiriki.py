import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import numpy as np
import datetime
from webdriver_manager.chrome import ChromeDriverManager

LOG_FILE_PATH = "mynavi.log"

### 模範解答から拝借 Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

### 模範解答から拝借 ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(LOG_FILE_PATH, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

### 模範解答から拝借 tableのthからtargetの文字列を探し一致する行のtdを返す
def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

### main処理
def main():
    log("処理開始")

    # 検索ワードを聞く
    search_word = input("検索ワードを入力してください >> ")
    log("検索キーワード:{}".format(search_word))

    # ブラウザを開く これだとbotだと丸わかりでブロックされてしまう
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    # 模範解答から拝借 driverを起動
    if os.name == 'nt': #Windows
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif os.name == 'posix': #Mac
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    
    # マイナビ転職のTOP画面を開く
    # driver.get("https://tenshoku.mynavi.jp/")

    # キーワード入力済のページを開く
    driver.get("https://tenshoku.mynavi.jp/list/kw" + search_word + "/?jobsearchType=14&searchType=18")

    # 3秒待機
    time.sleep(3)

    # ポップアップを閉じる動作 https://www.headboost.jp/python-try-except/
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(3)
        # ポップアップを閉じる2回目
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass # ポップアップが出ない場合は何も行わない

    # 検索ワードを入力してクリック
    # nyuryokuran = driver.find_element_by_class_name("topSearch__text")
    # nyuryokuran.send_keys(search_word)
    # driver.find_element_by_class_name("topSearch__button").click()

    # 3秒待機
    time.sleep(3)

    # 要素を格納するリストを用意
    # exp_shamei_list = []
    # exp_table_list = []
    exp_content_list = []
    exp_place_list = []
    exp_first_year_fee_list = []

    # ログ出力用の変数
    count = 1
    success = 0
    fail = 0

    # 要素を取得
    while True:
        # 会社名だけのパターン
        # shamei_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        # for shamei in shamei_list:
        #     exp_shamei_list.append(shamei.text)
        #     print(shamei.text)

        # テーブルの部分全てを取得する
        table_list = driver.find_elements_by_class_name("tableCondition")
        for table in table_list:
            try:
                # 全てをそのまま出力するパターン
                # exp_table_list.append(table.text)
                # print(table.text)
            
                # 模範解答から拝借した関数を使い、テーブルから仕事内容・勤務地・初年度年収を抜き出す
                content = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "仕事内容")
                exp_content_list.append(content)
                # print(content)
                
                place = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "勤務地")
                exp_place_list.append(place)
                # print(place)
                            
                first_year_fee = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                exp_first_year_fee_list.append(first_year_fee)
                # print(first_year_fee)

                log(f"{count}件目成功 : {content}")
                success+=1
            except Exception as e:
                log(f"{count}件目失敗 : {content}")
                log(e)
                fail+=1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count+=1
                      
        # ページ送りの矢印がある場合はそこをクリック　なくなった時点でbreak
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            log("最終ページです。終了します。")
            break
    
    df = pd.DataFrame({"仕事内容":exp_content_list,
                       "勤務地":exp_place_list,
                       "初年度年収":exp_first_year_fee_list})
    # インデックスを0ではなく1から割り振る https://chusotsu-program.com/df-reset-index/
    df.index = np.arange(1, len(df)+1)

    df.to_csv("mynavi.csv", encoding="utf-8-sig")
    log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")
    print("csvファイルを出力しました")

    # ブラウザを終了する。
    driver.close()

# モジュールとして呼び出された場合は起動せず、直接起動された場合のみmain()を起動する
if __name__ == "__main__":
    main()