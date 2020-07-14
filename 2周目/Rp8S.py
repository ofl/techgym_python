import random

players = []


class Player:
    def __init__(self, name, coin):
        self.name = name
        self.coin = coin

    def info(self):
        print(self.name + '：' + str(self.coin))

    def set_bet_coin(self, bet_coin):
        self.coin -= bet_coin
        print(self.name + 'は ' + str(bet_coin) + 'コイン BETしました。')


class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self):
        bet_message = '何枚BETしますか？：(1-99)'
        bet_coin = input(bet_message)
        while not self.enable_bet_coin(bet_coin):
            bet_coin = input(bet_message)
        super().set_bet_coin(int(bet_coin))

    def enable_bet_coin(self, string):
        if string.isdigit():
            number = int(string)
            if number >= 1 and number <= 99:
                return True
            else:
                return False
        else:
            return False


class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self):
        if self.coin >= 99:
            max_bet_coin = 99
        else:
            max_bet_coin = self.coin
        bet_coin = random.randint(1, max_bet_coin)
        super().set_bet_coin(bet_coin)


def create_players():
    global players
    human = Human('MY', 500)
    computer1 = Computer('C1', 500)
    computer2 = Computer('C2', 500)
    computer3 = Computer('C3', 500)
    players = [human, computer1, computer2, computer3]


def play():
    print('デバッグログ：play()')
    create_players()
    show_players()


def show_players():
    for player in players:
        player.info()

    for player in players:
        player.bet()

    for player in players:
        player.info()


play()
