import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

# Chromeを起動する関数


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

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # 仕事内容、給与、初年度年収のリストを作成
    exp_naiyou_list = []
    exp_kyuyo_list = []
    exp_nenshu_list = []
    
    # 3項目を50件目まで取得
    for i in range(1,51):
        xpath_naiyou = "/html/body/div[1]/div[3]/form/div/div["+str(i)+"]/div/div[2]/div[1]/table/tbody/tr[1]/td"
        naiyou_list = driver.find_elements_by_xpath(xpath_naiyou)
        for naiyou in naiyou_list:
            exp_naiyou_list.append(naiyou.text)
            print(naiyou.text)
        xpath_kyuyo = "/html/body/div[1]/div[3]/form/div/div["+str(i)+"]/div/div[2]/div[1]/table/tbody/tr[4]/td"
        kyuyo_list = driver.find_elements_by_xpath(xpath_kyuyo)
        for kyuyo in kyuyo_list:
            exp_naiyou_list.append(kyuyo.text)
            print(kyuyo.text)
        xpath_nenshu = "/html/body/div[1]/div[3]/form/div/div["+str(i)+"]/div/div[2]/div[1]/table/tbody/tr[5]/td"
        nenshu_list = driver.find_elements_by_xpath(xpath_nenshu)
        for nenshu in nenshu_list:
            exp_nenshu_list.append(nenshu.text)
            print(nenshu.text)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
