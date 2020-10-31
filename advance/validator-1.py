"""
ユーザー入力を抽象化するクラスを作成する
バリデーションを行う
"""

import re


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
            return f'例{self.__sample}のような値を入力してください'

# validator = RegexValidator(r'\w\d')
# validator.validate('A1')


class IncludesValidator(Validator):
    def __init__(self, valid_values):
        self.__valid_values = valid_values

    def is_valid(self, value):
        return value in self.__valid_values

    def error_message(self):
        list_ = map(str, self.__valid_values)
        return f'{(",").join(list_)}のいずれかを入力してください'


# validator = IncludesValidator([1, 2, 3])
# validator.validate(3)


class RangeValidator(Validator):
    def __init__(self, min_value, max_value):
        self.__min_value = min_value
        self.__max_value = max_value

    def is_valid(self, value):
        return self.__min_value <= value <= self.__max_value

    def error_message(self):
        return f'{self.__min_value} ~ {self.__max_value}の値を入力してください'


# validator = RangeValidator(10, 20)
# validator.validate(15)


class Hand:
    __HANDS = ['グー', 'チョキ', 'パー']

    def __init__(self, number):
        validator = IncludesValidator(list(range(len(self.__HANDS))))
        validator.validate(number)

        self.__number = number

    @classmethod
    def create_by_user_input(cls, string):
        return cls(int(string))

    @classmethod
    def waiting_input_message(cls):
        hands = []
        for i in range(len(cls.__HANDS)):
            hands.append(str(i) + ':' + cls.__HANDS[i])

        return f"あなたの手を入力してください({', '.join(hands)}):"

    @property
    def name(self):
        return self.__HANDS[self.__number]


class UserInput:
    def __init__(self, return_object_class):
        self.return_object_class = return_object_class

    def call(self):
        '''
        ユーザーの入力を元にreturn_object_classのインスタンスを作成して返す
        正しい値を受け取るまで入力待ちを繰り返す
        return_object_classにはクラスメソッドcreate_by_user_input()、waiting_input_message()を定義しておくこと
        '''
        while True:
            try:
                waiting_message = self.return_object_class.waiting_input_message()
                string = input(waiting_message)
                return self.return_object_class.create_by_user_input(string)

            except ValidationError as e:
                print(e.message)
            except (TypeError, ValueError):
                print('入力値が不正です')


if __name__ == '__main__':
    user_input = UserInput(Hand)
    hand = user_input.call()

    print(hand.name)
