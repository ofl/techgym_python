import random

print('じゃんけんスタート')

print('自分の手を入力してください')
my_hand = int(input('0:グー, 1:チョキ, 2:パー'))
you_hand = random.randint(0, 2)

result = my_hand - you_hand

if result == 0:
    print('あいこ')
elif result == 1 or result == -2:
    print('負け')
else:
    print('勝ち')
