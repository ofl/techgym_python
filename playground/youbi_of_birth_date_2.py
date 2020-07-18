import datetime

year = int(input("生まれた年を西暦で入力してください。"))
month = int(input("生まれた月を1~12の数字で入力してください。"))
date = int(input("生まれた日付を1~12の数字で入力してください。"))


def get_birth_date():
    birth_date = datetime.date(year, month, date)
    return birth_date


def get_day_of_week_jp(birth_date):
    week_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
    return week_list[birth_date.weekday()]


your_birth_date = get_birth_date()
your_day_of_week_jp = get_day_of_week_jp(your_birth_date)

print('あなたの生年月日は「' + str(your_birth_date) + '」ですね。')
print('あなたの生まれた曜日は「' + your_day_of_week_jp + '」ですね。')
