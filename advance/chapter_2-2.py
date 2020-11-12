'''間違い探し'''

from random import randrange
from math import ceil, floor
from time import time
import re

QUESTION_TEXT = '見貝土士眠眼己巳尤犬到致矢失白臼干千回同夭天二ニへヘ'


class Game:
    '''
    不正解かタイムオーバーを二回つづけるまでゲームを繰り返す
    '''

    TIMEOUT = 10

    def __init__(self, single_game_class):
        self._single_game_class = single_game_class
        self._level = Level()

    def play(self):
        last_result = True

        while True:
            start_at = time()
            game = self._single_game_class(self._level)
            game.play()

            interval = time() - start_at

            if game.is_success and interval <= self.TIMEOUT:
                print(game.success_message)
                self._level.up()
                last_result = True
            else:
                message = '時間ぎれです' if interval > self.TIMEOUT else game.failure_message
                print(message)

                if not last_result:
                    print('２回連続して失敗したのでゲームオーバー')
                    break

                self._level.down()
                last_result = False


class SpotTheDifference:
    '''間違い探しゲーム'''

    def __init__(self, level):
        self._level = level
        self._wrong_point = Point.create_randomly(level)
        self._matrix = Matrix(level, Question(), self._wrong_point)
        self.is_success = False

    def play(self):
        self._matrix.show()
        self._set_user_selected_point()
        self.is_success = self._wrong_point == self._user_selected_point

    @property
    def success_message(self):
        return '正解です'

    @property
    def failure_message(self):
        return f'間違いです 正解の座標:{Alphabet(self._wrong_point.x)}{self._wrong_point.y + 1}'

    def _set_user_selected_point(self):
        user_input = UserInput(Point)
        self._user_selected_point = user_input.call('座標を入力してください (例:A1) :')


class Level:
    def __init__(self, number=1):
        self.number = number

    def up(self):
        self.number += 1

    def down(self):
        if self.number > 1:
            self.number -= 1

    @property
    def row_size(self):
        return 2 + ceil(self.number / 2)

    @property
    def col_size(self):
        return 3 + floor(self.number / 2)


class Question:
    def __init__(self, text=QUESTION_TEXT):
        self._current_pair = self._get_question(text)

    @property
    def correct_char(self):
        return self._current_pair[0]

    @property
    def wrong_char(self):
        return self._current_pair[1]

    def _get_question(self, text):
        pairs = self._get_pairs(text)
        pair = pairs[randrange(len(pairs))]
        if randrange(2) < 2:
            # 1/2の確率でcorrectとwrongの組み合わせを入れ替える
            pair.reverse()
        return pair

    def _get_pairs(self, text):
        '''
        見貝土士眠眼 => [[見, 貝], [土, 士], [眠, 眼]]
        '''
        pairs = []
        for i in range(round(len(text)/2)):
            pair = text[i * 2:i * 2 + 2]
            pairs.append([pair[0], pair[1]])
        return pairs


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    @classmethod
    def create_by_user_input(cls, string):
        validator = RegexValidator(r'[a-zA-Z]\d+', 'A1')
        validator.validate(string)

        col_str, row_str = string[0], string[1:]
        return cls(Alphabet.index_of(col_str.lower()), int(row_str) - 1)

    @classmethod
    def create_randomly(cls, level):
        return cls(randrange(level.col_size), randrange(level.row_size))


class Matrix:
    def __init__(self, level: Level, question: Question, different_point: Point):
        self._level = level
        self._question = question
        self._wrong_point = different_point

    def show(self):
        rows = [self._header]
        for i in range(self._level.row_size):
            txt = f'{i+1} '
            for j in range(self._level.col_size):
                if self._wrong_point == Point(j, i):
                    txt += self._question.wrong_char
                else:
                    txt += self._question.correct_char
            rows.append(txt)
        print('\n'.join(rows))

    @property
    def _header(self):
        labels = Alphabet.LIST[:self._level.col_size]
        return f'  {" ".join(labels)}'


class Alphabet:
    LIST = [chr(i) for i in range(97, 97+26)]

    def __init__(self, number):
        self.char = self.LIST[number]

    def __str__(self):
        return self.char

    @classmethod
    def index_of(cls, character):
        return cls.LIST.index(character)


class UserInput:
    def __init__(self, return_object_class, validators=[]):
        self.__return_object_class = return_object_class

    def call(self, waiting_message):
        '''
        ユーザーの入力を元に__return_object_classのインスタンスを作成して返す
        正しい値を受け取るまで入力待ちを繰り返す
        __return_object_classにはクラスメソッドcreate_by_user_input()を定義しておくこと
        '''
        while True:
            try:
                string = input(waiting_message)
                return self.__return_object_class.create_by_user_input(string)

            except ValidationError as e:
                print(e.message)
            except (TypeError, ValueError):
                print('入力値が不正です')


class Validator:
    def validate(self, value):
        '''
        valueを検証して不正な値の場合はValidationErrorを発生させる
        '''
        if not self.is_valid(value):
            raise ValidationError(self.error_message())

    def is_valid(self, value):
        raise NotImplementedError

    def error_message(self,):
        raise NotImplementedError


class RegexValidator(Validator):
    def __init__(self, expression, sample=""):
        self.__expression = expression
        self.__sample = sample

    def is_valid(self, value):
        return re.search(self.__expression, value)

    def error_message(self):
        if self.__sample == '':
            return '書式が違います'
        else:
            return f'「{self.__sample}」のような値を入力してください'


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    game = Game(SpotTheDifference)
    game.play()
