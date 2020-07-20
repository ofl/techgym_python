# 「再帰」を使って繰り返しの処理を行ってみましょう。

import random


def loop():
    # ランダムで0~2の数字をnumに代入します。
    num = random.randint(0, 2)
    print(num)

    # numが2より少なければ
    if num < 2:
        loop()  # 自分自身を呼び出します（再帰）


loop()
