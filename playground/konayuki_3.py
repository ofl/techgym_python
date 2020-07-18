import time

konayuki = ['こ', 'な', 'ゆ', 'き']

for kana in konayuki:
    print(kana)
    if kana == 'な':
        time.sleep(3)
    else:
        time.sleep(0.5)
