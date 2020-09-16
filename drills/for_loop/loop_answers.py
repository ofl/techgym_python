# Drill 1の回答例

seasons = ['春', '夏', '秋', '冬']

for season in seasons:
    print(season)

# Drill 2の回答例

seasons = ['春', '夏', '秋', '冬']

for season in seasons:
    print('立' + season)

# Drill 3の回答例

seasons = ['春', '夏', '秋', '冬']

for season in seasons:
    if season == '冬':
        print('雪まつり')
    else:
        print(season + '祭り')

# Drill 4の回答例

seasons = ['春', '夏', '秋', '冬']
index = 1

for season in seasons:
    print(season + str(index) + '番')
    index += 1

# Drill 5の回答例

seasons = ['春', '夏', '秋', '冬']
text = ''

for season in seasons:
    text += season

print(text)

# Drill 6の回答例

seasons = ['春', '夏', '秋', '冬', '春', '夏', '秋', '冬']
index = 0

for season in seasons:
    if index % 2 == 1:
        print(season)
    index += 1

# Drill 7の回答例

seasons = ['春', '夏', '秋', '冬']
years = [2020, 2021, 2022]

for year in years:
    for season in seasons:
        print(str(year) + season)
