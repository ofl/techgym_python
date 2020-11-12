'''
1章の改良
単一責任の原則を意識してクラスを分割した
'''

import random


class Game:
    '''
    ユーザーが止めるまでゲームを続ける
    '''

    def __init__(self, single_game_class):
        self.__single_game_class = single_game_class

    def play(self):
        while True:
            life_game = LifeGame(self.__single_game_class)
            life_game.play()
            if self.__is_end():
                break

    def __is_end(self):
        user_input = UserInput(YesNo)
        return not user_input.call('続けますか' + YesNo.choice())


class LifeGame:
    '''
    参加者にライフを設定してどちらかのライフが尽きるまでゲームを続ける
    '''

    def __init__(self, single_game_class):
        self.__single_game_class = single_game_class
        self.__players = [Human('あなた'), Computer('コンピューター')]

    def play(self):
        self.__show_welcome_message()
        last_result_is_draw = False

        while True:
            single_game = self.__single_game_class(
                self.__players, last_result_is_draw)
            single_game.play()

            loser = single_game.looser
            if loser:
                last_result_is_draw = False
                loser.life -= 1
                self.__show_lives()
                if loser.life == 0:
                    break
            else:
                last_result_is_draw = True

    def __show_lives(self):
        """
        残りライフを表示
        """
        result = ''
        for player in self.__players:
            result += f'{player.name}のライフは{player.life}'
        print(result)

    def __show_welcome_message(self):
        print(f'{self.__single_game_class.NAME}、スタート！')


class RockPaperScissors:
    NAME = 'じゃんけん'

    def __init__(self, players, last_result_is_draw=False):
        self.__players = players
        self.__last_result_is_draw = last_result_is_draw
        self.looser = None

    def play(self):
        self.__show_start_message()

        for player in self.__players:
            player.set_hand()

        self.__show_hands()
        self.__fight()

        if self.looser:
            self.__show_result()

    def __fight(self):
        """
        勝敗を決める
        """
        if self.__players[0].hand > self.__players[1].hand:
            self.looser = self.__players[1]
        elif self.__players[0].hand < self.__players[1].hand:
            self.looser = self.__players[0]

    def __show_start_message(self):
        if self.__last_result_is_draw:
            print('あいこで')
        else:
            print('じゃんけんほい')

    def __show_hands(self):
        for player in self.__players:
            print(player.name + 'の手は ' + player.hand.name)

    def __show_result(self):
        if isinstance(self.looser, Human):
            print('あなたの負けです')
        else:
            print('あなたの勝ちです')


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.life = 3

    # 次に出す手を決定する(子クラスで定義すること)
    def set_hand(self):
        raise NotImplementedError


class Computer(Player):
    def set_hand(self):
        self.hand = Hand(random.randint(0, 2))


class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def set_hand(self):
        user_input = UserInput(Hand)
        self.hand = user_input.call(Hand.choice())


class Hand:
    __CHOICE = {0: 'グー', 1: 'チョキ', 2: 'パー'}

    def __init__(self, number):
        validator = ContainsValidator(self.__CHOICE.keys())
        validator.validate(number)

        self.name = self.__CHOICE[number]

    def __eq__(self, other):
        '''
        self == otherであいこと判定する
        '''
        return self.name == other.name

    def __gt__(self, other):
        '''
        self > otherで勝ちと判定する
        '''
        return (self.name, other.name) in [('グー', 'チョキ'), ('チョキ', 'パー'), ('パー', 'グー')]

    def __lt__(self, other):
        '''
        self < otherで負けと判定する
        '''
        return (self.name, other.name) in [('チョキ', 'グー'), ('パー', 'チョキ'), ('グー', 'パー')]

    @classmethod
    def create_by_user_input(cls, string):
        return cls(int(string))

    @classmethod
    def choice(cls):
        list_ = []
        for k, v in cls.__CHOICE.items():
            list_.append(f'{k}:{v}')

        return f"({', '.join(list_)}):"


class YesNo:
    __CHOICE = {'Y': 'はい', 'N': 'いいえ'}

    def __init__(self, string):
        validator = ContainsValidator(self.__CHOICE.keys())
        validator.validate(string)

        self.__yes_or_no = string

    def __bool__(self):
        return self.__yes_or_no == 'Y'

    @classmethod
    def create_by_user_input(cls, string):
        return cls(string.upper())

    @classmethod
    def choice(cls):
        list_ = []
        for k, v in cls.__CHOICE.items():
            list_.append(f'{k}:{v}')

        return f"({', '.join(list_)}):"


class UserInput:
    def __init__(self, return_object_class):
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


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


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


class ContainsValidator(Validator):
    '''
    イニシャライズ時に受け取ったリストに含まれる値以外の場合はValidationErrorを起こす
    '''

    def __init__(self, valid_values):
        self.__valid_values = valid_values

    def is_valid(self, value):
        return value in self.__valid_values

    def error_message(self):
        list_ = map(str, self.__valid_values)
        return f'{(",").join(list_)}のいずれかを入力してください'


if __name__ == '__main__':
    game = Game(RockPaperScissors)
    game.play()
