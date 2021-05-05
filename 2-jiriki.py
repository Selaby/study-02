from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time

# 模範解答から拝借 tableのthからtargetの文字列を探し一致する行のtdを返す
def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

### main処理
def main():
    # 検索ワードを聞く
    search_word = input("検索ワードを入力してください >> ")
    # ブラウザを開く。
    driver = webdriver.Chrome(executable_path='D:\Documents\OneDrive - 武内 健太朗\My Python\chromedriver.exe')
    # マイナビ転職のTOP画面を開く。
    driver.get("https://tenshoku.mynavi.jp/")
    # 3秒待機
    time.sleep(3)

    # ポップアップが出た（進めなくなった）場合は例外処理でポップアップを閉じる動作を経由する https://www.headboost.jp/python-try-except/
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(3)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass # ポップアップが出ない場合は何も行わない

    # 検索ワードを入力してクリック
    nyuryokuran = driver.find_element_by_class_name("topSearch__text")
    nyuryokuran.send_keys(search_word)
    driver.find_element_by_class_name("topSearch__button").click()

    # 3秒待機
    time.sleep(3)

    # 要素を格納するリストを用意
    # exp_shamei_list = []
    # exp_table_list = []
    exp_content_list = []
    exp_place_list = []
    exp_first_year_fee_list = []

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
            # 全てをそのまま出力するパターン
            # exp_table_list.append(table.text)
            # print(table.text)
        
        # 模範解答から拝借した関数を使い、テーブルから仕事内容・勤務地・初年度年収を抜き出す
            content = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "仕事内容")
            exp_content_list.append(content)
            print(content)
            
            place = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "勤務地")
            exp_place_list.append(place)
            print(place)
                        
            first_year_fee = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
            exp_first_year_fee_list.append(first_year_fee)
            print(first_year_fee)
            
        # 矢印がある場合はそこをクリック　なくなった時点でbreak
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            print("最終ページです。終了します。")
            break
                
    # # ログインIDを入力
    # login_id = driver.find_element_by_name("login")
    # login_id.send_keys("a254067772")
    # # 次へボタンをクリック
    # next_btn = driver.find_element_by_name("btnNext")
    # next_btn.click()
    # # 1秒待機
    # time.sleep(1)
    # # パスワードを入力
    # password = driver.find_element_by_name("passwd")
    # password.send_keys("7X2i7Yy6P86o74C9")
    # #ログインボタンをクリック
    # login_btn = driver.find_element_by_name("btnSubmit")
    # login_btn.click()
    # #10秒待機
    # time.sleep(10)
    # ブラウザを終了する。
    driver.close()

# モジュールとして呼び出された場合は起動せず、直接起動された場合のみmain()を起動する
if __name__ == "__main__":
    main()