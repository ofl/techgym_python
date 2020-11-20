import random
import sys
import math
import time


class DifferenceGame:
    __QUIZ_DATA = [['見', '貝'], ['土', '士'], ['眠', '眼'], ['己', '巳'], ['尤', '犬'],
                   ['到', '致'], ['斉', '斎'], ['棄', '菜'], ['矢', '失'], ['白', '臼'],
                   ['干', '千'], ['回', '同'], ['夭', '天'], ['二', 'ニ']]
    __MAX_LEVEL = 24
    __MIN_LEVEL = 5
    __TIME_LIMIT = 10  # sec
    __GAME_RESULTS = ['success', 'failure', 'timeout', 'invalid_input']

    def __init__(self):
        self.__level = 5
        self.__results = []
        self.__matrix = None
        self.__start_at = None

    def play(self):
        self.__setup()
        row, col = self.__get_player_input()
        self.__show_result(row, col)

    def show_start_message(self):
        print('1つだけ異なる漢字の番号を入力してください')
        # print('レベル:' + str(self.level))

    def __setup(self):
        self.__matrix = Matrix(self.__level, self.__QUIZ_DATA[0])
        self.__matrix.show()
        self.__start_at = time.time()

    def __show_result(self, row, col):
        if row is None or col is None:
            pass
        elif self.__matrix.is_correct_answer(row, col):
            print('正解です')
        else:
            print(f"正しい答えは{self.__matrix.correct_answer}です。")

    def __get_result(self, row, col):
        if row is None or col is None:
            return self.__GAME_RESULTS[3]
        elif self.__is_timeout():
            return self.__GAME_RESULTS[2]
        elif self.__matrix.is_correct_answer(row, col):
            return self.__GAME_RESULTS[0]
        else:
            return self.__GAME_RESULTS[1]

    def __level_up(self):
        if self.__level < self.__MAX_LEVEL:
            self.__level += 1
            print('レベルアップしました')

    def __level_down(self):
        if self.__level > self.__MIN_LEVEL:
            self.__level -= 1
            print('レベルダウンしました')

    def __reset_results(self):
        self.__results = []

    def __get_player_input(self):
        player_input = input('番号(例:A1)を入力:')
        col = self.__matrix.get_col_header(player_input[0])
        if col is None:
            print(self.__matrix.invalid_message_of_col)
        row = self.__matrix.get_row_header(player_input[1:])
        if row is None:
            print(self.__matrix.invalid_message_of_row)
        return row, col

    def __is_timeout(self):
        time.time() - self.__start_at > self.__TIME_LIMIT * 1000

    @property
    def __last_result(self):
        if len(self.__results) == 0:
            return None

        return self.__results[-1]


class Matrix:
    __ALPHABET = 'ABCDEFGHI'

    def __init__(self, size, kanji_pair):
        self.__size = size
        self.__mistake_num = random.randint(0, size * size - 1)
        self.__kanji_pair = kanji_pair

    #
    # '  A　B　C　D　E'
    # '1 土 土 土 土 土'
    # '2 土 土 土 土 土'
    #
    def show(self):
        print(f"   {'  '.join(self.__col_headers)}")

        for i in range(self.__size):
            rows = []
            for j in range(self.__size):
                index = self.__index_from_row_and_col(i, j)
                if self.__mistake_num == index:
                    rows.append(self.__kanji_pair[1])
                else:
                    rows.append(self.__kanji_pair[0])
            print(f"{self.__row_headers[i].ljust(2, ' ')} {' '.join(rows)}")

    def get_row_header(self, row_num):
        return self.__index_of(self.__row_headers, row_num)

    def get_col_header(self, alphabet):
        return self.__index_of(self.__col_headers, alphabet.upper())

    def is_correct_answer(self, row, col):
        index = self.__index_from_row_and_col(row, col)
        return index == self.__mistake_num

    @property
    def invalid_message_of_row(self):
        max = self.__row_headers[-1]
        min = self.__row_headers[0]
        return f"列は{min} ~ {max}の範囲で入力したください。"

    @property
    def invalid_message_of_col(self):
        max = self.__col_headers[-1]
        min = self.__col_headers[0]
        return f"行は{min} ~ {max}の範囲で入力したください。"

    @property
    def correct_answer(self):
        row = math.floor(self.__mistake_num / self.__size)
        col = self.__mistake_num % self.__size
        alphabet = self.__col_headers[col]
        num = self.__row_headers[row]
        return alphabet + num

    def __index_of(self, array, value):
        return array.index(value) if value in array else None

    def __index_from_row_and_col(self, row, col):
        return self.__size * row + col

    # => ['1', '2', '3',...]
    @property
    def __row_headers(self):
        return list(map(str, range(1, self.__size + 1)))

    # => ['A', 'B', 'C',...]
    @property
    def __col_headers(self):
        return list(self.__ALPHABET[0:self.__size])


if __name__ == '__main__':
    game = DifferenceGame()
    game.show_start_message()
    game.play()
