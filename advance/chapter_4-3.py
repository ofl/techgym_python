'''
Cellのリストを保持するCellListクラスを追加した
'''

import random


class BankruptcyGame(object):
    """
    参加者の誰かが破産(bankruptcy)するまでゲームを続ける
    """

    HUMAN_PLAYRES = ['MY']
    COMPUTER_PLAYRES = ['C1', 'C2', 'C3']

    def __init__(self, single_game_class):
        self.__single_game_class = single_game_class
        self.__players = self.__create_players()

    def play(self):
        while True:
            game = self.__single_game_class(self.__players)
            game.play()

            if self.__is_game_end:
                break

    @ property
    def __is_game_end(self):
        for player in self.__players:
            if player.is_bankruptcy:
                print(player.name + 'のコインがなくなったためゲームを終了します。')
                return True
        return False

    def __create_players(self):
        players = []
        for name in self.HUMAN_PLAYRES:
            players.append(Human(name, 500))
        for name in self.COMPUTER_PLAYRES:
            players.append(Computer(name, 500))
        return players


class CasinoGame:
    def __init__(self, players):
        self.__players = players
        self.__cells_list = CellList()
        self.__bets = []

    def play(self):
        self.__bet_coins()
        self.__show_table()
        self.__check_hit()
        self.__show_coin()

    def __show_coin(self):
        message = '[持ちコイン] '
        for player in self.__players:
            message += player.info
        print(message)

    def __find_bets_by_cell(self, hit_cell):
        bets = []
        for bet in self.__bets:
            if bet.cell == hit_cell:
                bets.append(bet)
        return bets

    def __bet_coins(self):
        for player in self.__players:
            self.__bets.append(player.make_bet(self.__cells_list))

    def __check_hit(self):
        roulette = Roulette(self.__cells_list)
        hit_cells = roulette.get_hit_cells()

        for hit_cell in hit_cells:
            hit_bets = self.__find_bets_by_cell(hit_cell)
            for bet in hit_bets:
                bet.win()

    def __show_table(self):
        table = Table(self.__cells_list, self.__players, self.__bets)
        table.show()


class Player:
    MAX_BET_COIN = 99

    def __init__(self, name, coin):
        self.name = name
        self.__coin = coin

    def make_bet(self, cell_list):
        raise NotImplementedError

    def create_bet(self, cell, bet_coin):
        self.__coin -= bet_coin
        bet = Bet(self, cell, bet_coin)
        print(bet.info)
        return bet

    def win_coin(self, coin):
        self.__coin += coin

    @property
    def info(self):
        return self.name + ':' + str(self.__coin) + ' / '

    @property
    def is_bankruptcy(self):
        return self.__coin <= 0

    @property
    def max_bet_coin(self):
        return min(self.__coin, self.MAX_BET_COIN)


class Human(Player):
    def make_bet(self, cell_list):
        bet_coin = self.__get_bet_coin()
        bet_cell = self.__get_bet_cell(cell_list)
        return super().create_bet(bet_cell, int(bet_coin))

    def __get_bet_coin(self):
        bet_message = '何枚BETしますか？：(1-' + str(self.max_bet_coin) + ')'
        while True:
            bet_coin = input(bet_message)
            if self.__enable_bet_coin(bet_coin):
                break
        return bet_coin

    def __get_bet_cell(self, cell_list):
        bet_message = 'どこにBETしますか？：(R,B,1-8)'
        while True:
            cell_name = input(bet_message)
            if self.__enable_cell_name(cell_name):
                cell = cell_list.find(cell_name)
                if cell:
                    break
        return cell

    def __enable_bet_coin(self, string):
        if not string.isdigit():
            return False

        number = int(string)
        return 0 < number and number <= self.max_bet_coin

    def __enable_cell_name(self, string):
        if string.isdigit():
            number = int(string)
            return 0 < number and number <= CellList.CELL_SIZE

        return string == 'R' or string == 'B'


class Computer(Player):
    def make_bet(self, cell_list):
        bet_coin = random.randint(1, self.max_bet_coin)
        bet_cell_number = random.randint(1, 8)
        cell = cell_list.find(str(bet_cell_number))
        return super().create_bet(cell, bet_coin)


class CellList:
    '''
    賭けの対象となるCellのリストを保持するオブジェクトを作成する
    '''
    CELL_SIZE = 8

    def __init__(self):
        self.cells = []
        self.__create_text_cells()
        self.__create_number_cells()

    def find(self, name):
        for cell in self.cells:
            if cell.name == name:
                return cell
        return None

    def __create_text_cells(self):
        for name in ['R', 'B']:
            self.cells.append(TextCell(name, 2))

    def __create_number_cells(self):
        for num in list(range(1, self.CELL_SIZE + 1)):
            self.cells.append(NumberCell(str(num), self.CELL_SIZE))


class Cell:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

    @property
    def color(self):
        raise NotImplementedError

    @property
    def title(self):
        return self.name + '(x' + str(self.rate) + ')'


class TextCell(Cell):
    @property
    def color(self):
        return 'red' if self.name == 'R' else 'black'


class NumberCell(Cell):
    @property
    def color(self):
        return 'red' if self.__is_odd else 'black'

    # 奇数かどうか？
    @property
    def __is_odd(self):
        return int(self.name) % 2 == 1


class Bet:
    def __init__(self, player, cell, coin):
        self.player = player
        self.cell = cell
        self.coin = coin

    def win(self):
        self.player.win_coin(self.returns)
        print(self.win_info)

    @property
    def info(self):
        return self.player.name + 'は ' + str(self.coin) + 'コイン を ' + self.cell.name + ' にBETしました。'

    @property
    def win_info(self):
        return self.player.name + 'は当たり ' + str(self.returns) + 'コインを獲得しました。'

    @property
    def returns(self):
        return self.coin * self.cell.rate


class Table:
    '''
    プレーヤーごとの賭けの状態を表示する
    '''

    def __init__(self, cell_list, players, bets):
        self.__cell_list = cell_list
        self.__players = players
        self.__bets = bets
        self.__output = ColorBase()

    def show(self):
        self.__show_header()
        self.__show_rows()

    def __show_header(self):
        columns = ['_____']
        for player in self.__players:
            columns.append(player.name)
        print(self.__get_decorated_row(columns))

    def __show_rows(self):
        for cell in self.__cell_list.cells:
            columns = [self.__get_colored_title(cell)]
            for player in self.__players:
                bet = self.__find_bet(cell, player)
                if bet:
                    columns.append(self.__get_colored_coin(bet))
                else:
                    columns.append('00')
            print(self.__get_decorated_row(columns))

    def __find_bet(self, cell, player):
        for bet in self.__bets:
            if bet.cell == cell and bet.player == player:
                return bet

        return None

    def __get_decorated_row(self, columns):
        divider = self.__output.paint_green('｜')
        return divider + divider.join(columns) + divider

    def __get_colored_title(self, cell):
        title = cell.title
        if cell.color == 'red':
            title = self.__output.paint_red(title)
        return title

    def __get_colored_coin(self, bet):
        zero_filled_coin = str(bet.coin).zfill(2)
        return self.__output.paint_yellow(zero_filled_coin)


class Roulette:
    def __init__(self, cell_list):
        self.__cell_list = cell_list

    def get_hit_cells(self):
        number_cell = self.__get_hit_number_cell()
        print('選ばれたのは「' + number_cell.name + '」')
        # 「R」「B」いずれかのセルも当たりに加えて返す。
        text_cell = self.__get_hit_text_cell(number_cell.color)
        return [number_cell, text_cell]

    def __get_hit_number_cell(self):
        # 数字のみを抽選したいため1~8のうち一つをひく
        num = random.randint(1, 8)
        return self.__cell_list.find(str(num))

    def __get_hit_text_cell(self, color):
        # セルの辞書からcolorの最初の文字を大文字にしたkeyの値を探す
        return self.__cell_list.find(color[0:1].upper())


class ColorBase:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    END = '\033[0m'

    def paint_red(self, string):
        return self.RED + string + self.END

    def paint_green(self, string):
        return self.GREEN + string + self.END

    def paint_yellow(self, string):
        return self.YELLOW + string + self.END


if __name__ == '__main__':
    game = BankruptcyGame(CasinoGame)
    game.play()
