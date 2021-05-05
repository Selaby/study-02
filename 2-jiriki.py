from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time

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

# 会社名を格納するリストを用意
exp_shamei_list = []

# 会社名を取得
while True:
    shamei_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    for shamei in shamei_list:
        exp_shamei_list.append(shamei.text)
        print(shamei.text)

    # next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
    # if len(next_page) >= 1:
    #     driver.find_element_by_class_name("iconFont--arrowLeft").click()
    # else:
    #     print("最終ページです。終了します。")
    #     break

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