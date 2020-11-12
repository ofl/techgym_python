'''
1章の改良
複数の人数でジャンケンして勝ち抜できるようにする
'''

import random


class RockPaperScissors:
    __MAX_ROUND = 20
    __NUMBER_OF_COMPUTER_PLAYERS = 5

    def __init__(self):
        self.__round = 1
        self.__is_draw = False
        self.__players = []

    def show_welcome_message(self):
        print('じゃんけんゲームにようこそ\n')

    def setup(self):
        self.__players.append(Human('あなた'))
        for i in range(self.__NUMBER_OF_COMPUTER_PLAYERS):
            self.__players.append(Computer('コンピューター' + str(i + 1)))

    def play(self):
        self.__show_start_message()

        for player in self.__players:
            player.set_hand()

        self.__throw_hands()
        self.__show_hands()
        self.__set_result()
        self.__show_result()

    @property
    def is_not_game_end(self):
        # 最大ラウンドを超えるか、残りが一人になるまで続ける
        return self.__round < self.__MAX_ROUND + 1 and len(self.__players) > 1

    def __show_start_message(self):
        print(f"{str(self.__round)}回戦")

    def __throw_hands(self):
        if self.__is_draw:
            print('あいこで')
        else:
            print('じゃんけん')

        print('ほい\n')

    def __show_hands(self):
        for player in self.__players:
            print(f"{player.name}の手は「{player.hand.name}」")

    def __set_result(self):
        hands = []
        for player in self.__players:
            hands.append(player.hand)

        losers = []
        for player in self.__players:
            if player.hand.is_loser(hands):
                losers.append(player)

        winners = list(set(self.__players) - set(losers))

        # 勝ち抜け人数が参加者と同数なら引き分け
        self.__is_draw = len(winners) == len(self.__players)
        self.__players = sorted(winners)
        self.__round += 1

    def __show_result(self):
        if not self.__is_draw:
            if len(self.__players) == 1:
                print(f"{self.__players[0].name}の優勝")
                return

            names = []
            for player in self.__players:
                names.append(player.name)
            print(f"{','.join(names)}の勝ち抜け")
        print('')


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = None

    # 次に出す手を決定する(子クラスで定義すること)
    def set_hand(self):
        raise NotImplementedError

    # sorted()でPlayerの並び順を名前にするため
    def __lt__(self, other):
        # self < other
        return self.name < other.name


class Computer(Player):
    def set_hand(self):
        self.hand = Hand(random.randint(0, 2))


class Human(Player):
    def __init__(self, name):
        super().__init__(name)
        self.__validator = Validator.create_integer_validator(0, 2)

    def set_hand(self):
        is_valid = False

        # 入力された文字が正しい値をとるまで繰り返し
        while not is_valid:
            player_input = input('次に出す手を入力してください。ex. (0:グー, 1:チョキ, 2:パー)')
            is_valid = self.__validator.is_valid(player_input)
            if not is_valid:
                print("0 ~ 2のいずれかの数字を入力してください")

        self.hand = Hand(int(player_input))


class Hand:
    __HANDS = ['グー', 'チョキ', 'パー']
    __RESULT = ['引き分け', '負け', '勝ち']

    def __init__(self, num):
        self.num = num

    def is_loser(self, other_hands=[]):
        results = []
        for other_hand in other_hands:
            results.append(self.__result(other_hand))

        # 結果の中に「負け」が存在して、「勝ち」が存在しなければ敗退
        return self.__RESULT[1] in results and self.__RESULT[2] not in results

    @property
    def name(self):
        return self.__HANDS[self.num]

    def __result(self, other_hand):
        return self.__RESULT[(self.num - other_hand.num)]


class Validator:
    def __init__(self, valid_list):
        self.__valid_list = valid_list

    @classmethod
    def create_integer_validator(cls, min, max):
        valid_list = list(map(str, range(min, max + 1)))
        return cls(valid_list)

    def is_valid(self, value):
        return value in self.__valid_list


if __name__ == '__main__':
    rps = RockPaperScissors()
    rps.show_welcome_message()
    rps.setup()

    while rps.is_not_game_end:
        rps.play()
