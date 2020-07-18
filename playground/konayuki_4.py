import time

konayuki = ['こ', 'な', 'ゆ', 'き']


def kakikae_print(text):
    print("\r" + text, end="")


for kana in konayuki:
    kakikae_print(kana)
    if kana == 'な' or kana == 'き':
        time.sleep(3)
    else:
        time.sleep(0.5)
