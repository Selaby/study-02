### 検索ツールサンプル
### これをベースに課題の内容を追記してください
import pandas as pd
import os
# カレントディレクトリを指定する
os.chdir("D://Documents//OneDrive - 武内 健太朗//My Python//課題")
df = pd.read_csv("list.csv")
source = list(df["name"])

### 検索ツール
def search():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")

    if word in source:
        print("{}が見つかりました".format(word))
        print(source)
    else:
        print("{}が見つかりませんでした".format(word))
        #リストになかった場合に、キャラクターをsourceに追加出来るようにする
        add_flag = input("追加登録しますか？ >>> (しない：0　する：1)")
        if add_flag == "1":
            source.append(word)
            # リストを再度データフレームに
            df = pd.DataFrame(source,columns=["name"])
            df.to_csv("newlist.csv", encoding="utf_8-sig")
            print("新しいリストを出力しました")
    
if __name__ == "__main__":
    search()
