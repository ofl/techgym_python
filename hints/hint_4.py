# ifやelseを使って条件を分岐してみましょう。


age = int(input("年齢を入力してください。"))
gender = int(input("性別は？(0: 男性、1: 女性)。"))


if age >= 20:
    adult_text = '成人した'
else:
    adult_text = '未成年の'

if gender < 1:
    gender_text = '男性ですね。'
else:
    gender_text = '女性ですね。'

print(adult_text + gender_text)
