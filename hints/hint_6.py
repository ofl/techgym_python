# 「関数」を作ってみましょう。

# 1. 引数も返り値もないもの


def hello_1():
    print('こんにちは')


hello_1()

# 2. func(xxx)のような引数があるもの


def hello_2(name):
    print(name + 'さんこんにちは')


hello_2('田中')

# 3. 関数を実行すると呼び出し元に値（返り値）を返すもの


def hello_3():
    return '山本さんこんにちは'


print(hello_3())

# 4. 引数と返り値があるもの


def hello_4(name):
    return name + 'さんこんにちは'


print(hello_4('山口'))

# 5. 引数は複数設定できます


def hello_5(name_1, name_2, name_3):
    return name_1 + 'さん' + name_2 + 'さん' + name_3 + 'さん' + 'こんにちは'


print(hello_5('木村', '井上', '竹田'))
