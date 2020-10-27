# 中原くんの回答を参考にした

'''間違い探し'''

from random import randrange
from math import ceil, floor

ALPHABET = [chr(i) for i in range(97, 97+26)]
QUESTION_TEXT = '見貝土士眠眼己巳尤犬到致矢失白臼干千回同夭天二ニへヘ'


class SpotTheDifference:
    '''間違い探しゲーム'''

    def __init__(self, text, level=1):
        self.matrix = Matrix(level)
        self._data = self._get_data(text)

        self._current_pair = None
        self._different_point = Point()
        self._user_selected_point = Point()

    def play(self):
        self._set_current_pair()
        self._set_different_point()
        self.matrix.show(self._current_pair, self._different_point)
        self._set_user_selected_point()

    def is_success(self):
        return self._different_point == self._user_selected_point

    def success_message(self):
        return '正解です'

    def failure_message(self):
        return f'間違いです 正解の座標:{ALPHABET[self._different_point.y]}{self._different_point.x + 1}'

    def _get_data(self, text):
        return [[text[i*2+j]for j in range(2)]
                for i in range(round(len(text)/2))]

    def _set_current_pair(self):
        rand = randrange(len(self._data))
        self._current_pair = self._data[rand]
        self._data.pop(rand)

    def _set_different_point(self):
        self._different_point.new(randrange(self.matrix.col),
                                  randrange(self.matrix.row))

    def _set_user_selected_point(self):
        while True:
            text = input('座標を入力してください (例:A1) :')
            if len(text) == 2:
                try:
                    choice = Point(text[0], text[1]) - Point(1, 1)
                except TypeError:
                    pass
                else:
                    if 0 <= choice.x < self.matrix.col and 0 <= choice.y < self.matrix.row:
                        self._user_selected_point = choice
                        break


class Matrix:
    def __init__(self, level):
        self._set_size(level)

    def show(self, current_pair, different_point):
        txt = ''
        txt += self._header()
        for i in range(self.row):
            txt += self._row_header(i)
            for j in range(self.col):
                if different_point == Point(j, i):
                    txt += current_pair[1]
                else:
                    txt += current_pair[0]
            txt += '\n'
        print(txt.rstrip('\n'))

    def _set_size(self, level):
        difficult = self._get_difficult()
        self.row = difficult[level]['row']
        self.col = difficult[level]['col']

    def _get_difficult(self):
        difficult = {}
        for i in range(13):
            difficult[i+1] = {'col': ceil(i/2)+3,
                              'row': floor(i/2)+3}
        return difficult

    def _header(self):
        return '  ' + ' '.join(ALPHABET[:self.col]) + '\n'

    def _row_header(self, i):
        return str(i+1) + ' '


class Point:
    '''class point\n
    x,y >= 0'''

    def __init__(self, x=0, y=0):
        self.new(x, y)

    def __eq__(self, obj):
        return obj.x == self._x and obj.y == self._y

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __add__(self, obj):
        return Point(self._x + obj.x, self._y + obj.y)

    def __sub__(self, obj):
        return Point(self._x - obj.x, self._y - obj.y)

    def __str__(self):
        return f'x:{self._x} y:{self._y}'

    @ staticmethod
    def _alpha2num(alpha):
        if isinstance(alpha, int):
            return alpha
        if alpha.isdecimal():
            return int(alpha)
        if len(alpha) != 1:
            raise TypeError()
        return ord(alpha.upper()) - ord('A') + 1

    def new(self, x, y):
        '''set'''
        self._x = self._alpha2num(x)
        self._y = self._alpha2num(y)

    def set_(self, x, y):
        '''set'''
        self.new(x, y)

    def get(self):
        '''return x, y'''
        return (self._x, self._y)

    @ property
    def x(self):
        '''x'''
        return self._x

    @ property
    def y(self):
        '''y'''
        return self._y


class Game:
    def __init__(self, single_game_class=SpotTheDifference, text=QUESTION_TEXT):
        self.single_game_class = single_game_class
        self._text = text
        self._level = 1

    def play(self):
        for i in range(13):
            game = self.single_game_class(self._text, self._level)
            game.play()
            if game.is_success():
                print(game.success_message())
            else:
                print(game.failure_message())
                break

            self._level += 1
        print(f'\n得点:{ceil(100/13*i)}')


if __name__ == "__main__":
    game = Game()
    game.play()
