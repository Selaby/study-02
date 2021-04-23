import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime


LOG_FILE_PATH = "mynavi.log"

### Chromeを起動する関数
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

### ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(LOG_FILE_PATH, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理
def main():
    log("処理開始")
    search_keyword = input("検索キーワードを入力　＞＞　")
    log("検索キーワード:{}".format(search_keyword))
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    # 例外処理 https://www.headboost.jp/python-try-except/
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass # ポップアップが出ない場合は何も行わない
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # 仕事内容、給与、初年度年収のリストを作成
    exp_naiyou_list = []
    exp_kyuyo_list = []
    exp_nenshu_list = []
    
    # ログ出力用の変数
    count = 1
    success = 0
    fail = 0

    # 3項目を50件目まで取得
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

        # 1ページ分繰り返し
        for table in table_list:
            try:
            # try~exceptはエラーの可能性が高い箇所に配置                
                # 3項目をtableから探す
                naiyou = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "仕事内容")
                exp_naiyou_list.append(naiyou)
                kyuyo = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "給与")
                exp_kyuyo_list.append(kyuyo)
                nenshu = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                exp_nenshu_list.append(nenshu)
                log(f"{count}件目成功 : {naiyou}")
                success+=1
            except Exception as e:
                log(f"{count}件目失敗 : {naiyou}")
                log(e)
                fail+=1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count+=1

        # ページ送り    
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            log("最終ページです。終了します。")
            break
    
    df = pd.DataFrame({"仕事内容":exp_naiyou_list,
                       "給与":exp_kyuyo_list,
                       "初年度年収":exp_nenshu_list})
    df.to_csv("mynavi.csv", encoding="utf-8-sig")
    log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")
    print("csvファイルを出力しました")
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
