# 「if」や「elif」や「else」を使って条件を分岐してみましょう。


age = int(input("年齢を入力してください。"))
gender = int(input("性別は？(0: 男性、1: 女性、3: 未回答)。"))


if age >= 20:
    adult_text = '成人した'
else:
    adult_text = '未成年の'

if gender == 0:
    gender_text = '男性ですね。'
elif gender == 1:
    gender_text = '女性ですね。'
else:
    gender_text = '性別不明な方ですね。'

print(adult_text + gender_text)
