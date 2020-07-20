# 「and」や「or」を使ってifの条件を組み合わせましょう。


age = int(input("年齢を入力してください。"))
drive = int(input("運転免許は持っていますか？(0: はい、1: いいえ)。"))

if age >= 18 and drive < 1:
    print('車の運転ができますね。')

    if age < 26 or age >= 85:
        print('運転には特に気をつけましょう。')
elif age >= 18:
    print('もう車の運転免許をとれますね。')
else:
    print('まだ車の運転免許はとれませんね。')
