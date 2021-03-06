'''
1章の改良
クラス化した
'''

import random
import time


class RockPaperScissors:
    __HANDS = ['グー', 'チョキ', 'パー']
    __RESULT_MESSAGES = ['引き分けです\n', 'あなたの勝ちです', 'あなたの負けです']

    def __init__(self):
        self.__computer_hand = None
        self.__player_hand = None
        # コンピュータの手から自分の手を引いた数を3で割った余りの数
        self.__modulo = None

    def show_welcome_message(self):
        print('じゃんけん、スタート！')

    def play(self):
        self.__show_start_message()

        self.__set_computer_hand()
        self.__set_player_hand()
        self.__set_modulo()

        self.__show_result()

    @property
    def is_not_game_end(self):
        return self.__is_first_game or self.__is_draw

    def __show_start_message(self):
        if self.__is_draw:
            print('あいこで')
        else:
            print('じゃんけん')
        time.sleep(1)

        print('ほい\n')
        time.sleep(1)

    # 標準入力からプレイヤーの選択した手(0~2までの文字)を受け取り数値に変換して返す
    def __set_player_hand(self):
        print('あなたの手を入力してください')
        is_valid = False
        message = self.__waiting_message

        # 入力された文字が正しい値をとるまで繰り返し
        while not is_valid:
            player_input = input(message)
            is_valid = self.__is_valid(player_input)
            if not is_valid:
                print(f"0 ~ {self.__index_of_last_hand}のいずれかの数字を入力してください")
        self.__player_hand = int(player_input)

    def __set_computer_hand(self):
        self.__computer_hand = random.randint(0, self.__index_of_last_hand)

    def __set_modulo(self):
        difference = self.__computer_hand - self.__player_hand
        self.__modulo = difference % self.__len_of_hand_list

    def __show_result(self):
        print('あなたの手は ' + self.__HANDS[self.__player_hand])
        print('コンピュータの手は ' + self.__HANDS[self.__computer_hand])
        time.sleep(1)

        print(self.__RESULT_MESSAGES[self.__modulo])

    def __is_valid(self, value):
        # 入力された値が「0」か「1」か「2」のいずれかの文字であるを判定
        return value in list(map(str, range(self.__len_of_hand_list)))

    # あいこかどうか
    @property
    def __is_draw(self):
        return self.__modulo == 0

    @property
    def __is_first_game(self):
        return self.__modulo == None

    @property
    def __len_of_hand_list(self):
        return len(self.__HANDS)

    @property
    def __index_of_last_hand(self):
        return self.__len_of_hand_list - 1

    # 入力待ちのメッセージ。ex. (0:グー, 1:チョキ, 2:パー)　:
    @property
    def __waiting_message(self):
        # mapを使う方が簡潔に書けるかもしれないが、読みづらいため
        hands = []
        for i in range(self.__len_of_hand_list):
            hands.append(str(i) + ':' + self.__HANDS[i])

        text = ', '.join(hands)
        return f"({text})　:"


if __name__ == '__main__':
    rps = RockPaperScissors()
    rps.show_welcome_message()

    while rps.is_not_game_end:
        rps.play()
