# Drill 1の回答例

seasons = ['春', '夏', '秋', '冬']
i = 0
while i < len(seasons):
    print(seasons[i])
    i += 1

# Drill 2の回答例

seasons = ['春', '夏', '秋', '冬']
i = 0
while i < len(seasons):
    print('立' + seasons[i])
    i += 1

# Drill 3の回答例

seasons = ['春', '夏', '秋', '冬']
i = 0
while i < len(seasons):
    if seasons[i] == '冬':
        print('雪まつり')
    else:
        print(seasons[i] + '祭り')
    i += 1

# Drill 4の回答例

seasons = ['春', '夏', '秋', '冬']
i = 0
while i < len(seasons):
    print(seasons[i] + str(i + 1) + '番')
    i += 1

# Drill 5の回答例

seasons = ['春', '夏', '秋', '冬']
text = ''
i = 0
while i < len(seasons):
    text += seasons[i]
    i += 1

print(text)

# Drill 6の回答例

seasons = ['春', '夏', '秋', '冬', '春', '夏', '秋', '冬']
i = 0

while i < len(seasons):
    if i % 2 == 1:
        print(seasons[i])
    i += 1

# Drill 7の回答例

seasons = ['春', '夏', '秋', '冬']
years = [2020, 2021, 2022]
i = 0
j = 0

while i < len(years):
    while j < len(seasons):
        print(str(years[i]) + seasons[j])
        j += 1
    i += 1
    j = 0
