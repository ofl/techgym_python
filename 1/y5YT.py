import random

print('じゃんけんスタート')

print('自分の手を入力してください')
my_hand = int(input('0:グー, 1:チョキ, 2:パー'))
your_hand = random.randint(0, 2)

if my_hand == 0:
    if your_hand == 0:
        print('あいこ')
    elif your_hand == 1:
        print('勝ち')
    elif your_hand == 2:
        print('負け')
elif my_hand == 1:
    if your_hand == 0:
        print('負け')
    elif your_hand == 1:
        print('あいこ')
    elif your_hand == 2:
        print('勝ち')
elif my_hand == 2:
    if your_hand == 0:
        print('勝ち')
    elif your_hand == 1:
        print('負け')
    elif your_hand == 2:
        print('あいこ')
