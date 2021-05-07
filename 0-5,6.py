def hello():
    print("Hello!")

hello()


name=["たんじろう","ぎゆう","ねずこ","むざん"]
name.append("ぜんいつ")
def namae(name1):
    if name1 in name:
        print(name1, "は含まれます")
    else:
        print(name1, "は含まれません")

namae("ぜんいす")