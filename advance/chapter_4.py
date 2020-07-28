import random


class Player:
    def __init__(self, name, coin):
        self.name = name
        self.coin = coin
        self.bets = {}
        self.reset_table()

    def set_bet_coin(self, bet_coin, bet_cell):
        self.coin -= bet_coin
        self.bets[bet_cell] = bet_coin
        print(self.name + 'は ' + str(bet_coin) +
              'コイン を ' + bet_cell + ' にBETしました。')

    def reset_table(self):
        self.bets = {}


class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self, _cell_names):
        if self.coin >= 99:
            max_bet_coin = 99
        else:
            max_bet_coin = self.coin
        bet_message = '何枚BETしますか？：(1-' + str(max_bet_coin) + ')'
        bet_coin = input(bet_message)
        while not self.enable_bet_coin(bet_coin, max_bet_coin):
            bet_coin = input(bet_message)

        bet_message = 'どこにBETしますか？：(R,B,1-8)'
        bet_cell = input(bet_message)
        while not self.enable_bet_cell(bet_cell):
            bet_cell = input(bet_message)

        super().set_bet_coin(int(bet_coin), bet_cell)

    def enable_bet_coin(self, string, max_bet_coin):
        if string.isdigit():
            number = int(string)
            if number >= 1 and number <= max_bet_coin:
                return True
            else:
                return False
        else:
            return False

    def enable_bet_cell(self, string):
        if string.isdigit():
            number = int(string)
            if number >= 1 and number <= 8:
                return True
            else:
                return False
        else:
            if string == 'R' or string == 'B':
                return True
            else:
                return False


class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self, cell_names):
        if self.coin >= 99:
            max_bet_coin = 99
        else:
            max_bet_coin = self.coin
        bet_coin = random.randint(1, max_bet_coin)

        bet_cell_number = random.randint(0, len(cell_names) - 1)
        bet_cell = cell_names[bet_cell_number]
        super().set_bet_coin(bet_coin, bet_cell)


class Cell:
    def __init__(self, name, rate, color):
        self.name = name
        self.rate = rate
        self.color = color


class Table:
    def __init__(self):
        self.cells = []
        self.create_table()

    def create_table(self):
        self.cells.append(Cell('R', 8, 'red'))
        self.cells.append(Cell('B', 8, 'black'))
        self.cells.append(Cell('1', 2, 'red'))
        self.cells.append(Cell('2', 2, 'black'))
        self.cells.append(Cell('3', 2, 'red'))
        self.cells.append(Cell('4', 2, 'black'))
        self.cells.append(Cell('5', 2, 'red'))
        self.cells.append(Cell('6', 2, 'black'))
        self.cells.append(Cell('7', 2, 'red'))
        self.cells.append(Cell('8', 2, 'black'))

    def show(self, players):
        row = self.green_bar() + '____' + self.green_bar()
        for player in players:
            row += player.name + self.green_bar()
        print(row)

        for cell in self.cells:
            row = self.green_bar() + self.color(cell.color, cell.name +
                                                '(x' + str(cell.rate) + ')') + self.green_bar()
            for player in players:
                if cell.name in player.bets:
                    row += str(player.bets[cell.name]
                               ).zfill(2) + self.green_bar()
                else:
                    row += '00' + self.green_bar()

            print(row)

    def green_bar(self):
        return self.color('green', '｜')

    def color(self, color_name, string):
        if color_name == 'red':
            return ColorBase.RED + string + ColorBase.END
        elif color_name == 'green':
            return ColorBase.GREEN + string + ColorBase.END
        else:
            return string

    @property
    def cell_names(self):
        names = []
        for cell in self.cells:
            names.append(cell.name)
        return names


class ColorBase:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    END = '\033[0m'


class CasinoGame:
    def __init__(self):
        self.players = []
        self.table = Table()

    def create_players(self):
        human = Human('MY', 500)
        computer1 = Computer('C1', 500)
        computer2 = Computer('C2', 500)
        computer3 = Computer('C3', 500)
        self.players = [human, computer1, computer2, computer3]

    def bet_players(self):
        for player in self.players:
            player.bet(self.table.cell_names)

    def check_hit(self):
        hit_cell_number = random.randint(0, len(self.table.cell_names) - 1)
        hit_cell = self.table.cell_names[hit_cell_number]
        print('選ばれたのは「' + hit_cell + '」')
        for player in self.players:
            if hit_cell in player.bets and player.bets[hit_cell] >= 1:
                self.win_player(player, hit_cell_number)

    def win_player(self, player, hit_cell_number):
        hit_cell = self.table.cell_names[hit_cell_number]
        win_coin = player.bets[hit_cell] * \
            self.table.cells[hit_cell_number].rate
        player.coin += win_coin
        print(player.name + 'は当たり ' + str(win_coin) + 'コインを獲得しました。')

    def show_coin(self):
        message = '[持ちコイン] '
        for player in self.players:
            message += player.name + ':' + str(player.coin) + ' / '
        print(message)

    def reset_table(self):
        for player in self.players:
            player.reset_table()

    def initialize(self):
        self.create_players()

    def play_once(self):
        self.reset_table()
        self.bet_players()
        self.table.show(self.players)
        self.check_hit()
        self.show_coin()

    def is_game_end(self):
        for player in self.players:
            if player.coin <= 0:
                return True
        return False

    def game_end(self):
        for player in self.players:
            if player.coin <= 0:
                print(player.name + 'のコインがなくなったためゲームを終了します。')

    def play(self):
        self.initialize()
        self.show_coin()
        while not self.is_game_end():
            self.play_once()
        else:
            self.game_end()


casino = CasinoGame()
casino.play()
