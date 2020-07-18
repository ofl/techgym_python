import datetime

WEEK_LIST = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']

year = int(input("生まれた年を西暦で入力してください。"))
month = int(input("生まれた月を1~12の数字で入力してください。"))
date = int(input("生まれた日付を1~12の数字で入力してください。"))

birth_date = datetime.date(year, month, date)
print('あなたの生年月日は「' + str(birth_date) + '」ですね。')

day_of_week_jp = WEEK_LIST[birth_date.weekday()]
print('あなたの生まれた曜日は「' + day_of_week_jp + '」ですね。')
