import random


class Player:
    MAX_BET_COIN = 99

    def __init__(self, name, coin):
        self.name = name
        self.__coin = coin

    def create_bet(self, bet_coin, cell):
        self.__coin -= bet_coin

        bet = Bet(self.name, cell.name, cell.rate, bet_coin)
        print(bet.info)
        return bet

    def win(self, bet):
        self.__coin += bet.win_coin
        print(bet.win_info)

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
    def get_bet(self, cell_dict):
        bet_coin = self.__get_bet_coin()
        cell_name = self.__get_bet_cell_name()

        return super().create_bet(int(bet_coin), cell_dict[cell_name])

    def __get_bet_coin(self):
        bet_message = '何枚BETしますか？：(1-' + str(self.max_bet_coin) + ')'
        while True:
            bet_coin = input(bet_message)
            if self.__enable_bet_coin(bet_coin):
                break
        return bet_coin

    def __get_bet_cell_name(self):
        bet_message = 'どこにBETしますか？：(R,B,1-8)'
        while True:
            cell_name = input(bet_message)
            if self.__enable_cell_name(cell_name):
                break
        return cell_name

    def __enable_bet_coin(self, string):
        if not string.isdigit():
            return False

        number = int(string)
        return 0 < number and number <= self.max_bet_coin

    def __enable_cell_name(self, string):
        if string.isdigit():
            number = int(string)
            return 0 < number and number <= CasinoGame.CELL_SIZE

        return string == 'R' or string == 'B'


class Computer(Player):
    def get_bet(self, cell_dict):
        bet_coin = random.randint(1, self.max_bet_coin)
        bet_cell_number = random.randint(0, 8)
        cell = cell_dict[str(bet_cell_number + 1)]
        return super().create_bet(bet_coin, cell)


class Cell:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.__output = ColorBase()

    @property
    def title(self):
        if self.color == 'red':
            return self.__output.paint_red(self.__name_and_rate)
        return self.__name_and_rate

    @property
    def color(self):
        raise NotImplementedError

    @property
    def __name_and_rate(self):
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


class Table:
    def __init__(self, cells, players, bets):
        self.__cells = cells
        self.__players = players
        self.__bets = bets
        self.__output = ColorBase()

    def show(self):
        self.__show_header()
        self.__show_rows()

    def __show_header(self):
        columns = ['____']
        for player in self.__players:
            columns.append(player.name)
        print(self.__get_decorated_row(columns))

    def __show_rows(self):
        for cell in self.__cells:
            columns = [cell.title]
            for player in self.__players:
                bet = self.__find_bet(cell.name, player.name)
                coin = bet.decorated_coin if bet else '00'
                columns.append(coin)
            print(self.__get_decorated_row(columns))

    def __find_bet(self, cell_name, player_name):
        for bet in self.__bets:
            if bet.cell_name == cell_name and bet.player_name == player_name:
                return bet

        return None

    def __get_decorated_row(self, columns):
        divider = self.__output.paint_green('｜')
        return divider + divider.join(columns) + divider


class Roulette:
    def __init__(self, cells):
        self.__cells = cells

    def get_hit_cells(self):
        number_cell = self.__get_hit_number_cell()
        print('選ばれたのは「' + number_cell.name + '」')
        # 「R」「B」いずれかのセルも当たりに加えて返す。
        text_cell = self.__get_hit_text_cell(number_cell.color)
        return [number_cell, text_cell]

    def __get_hit_number_cell(self):
        # 数字のみを抽選したいため1~8のうち一つをひく
        num = random.randint(1, 8)
        return self.__cells[str(num)]

    def __get_hit_text_cell(self, color):
        # セルの辞書からcolorの最初の文字を大文字にしたkeyの値を探す
        return self.__cells[color[0:1].upper()]


class Bet:
    def __init__(self, player_name, cell_name, rate, coin):
        self.player_name = player_name
        self.cell_name = cell_name
        self.coin = coin
        self.rate = rate
        self.__output = ColorBase()

    @property
    def info(self):
        return self.player_name + 'は ' + str(self.coin) + 'コイン を ' + self.cell_name + ' にBETしました。'

    @property
    def win_info(self):
        return self.player_name + 'は当たり ' + str(self.win_coin) + 'コインを獲得しました。'

    @property
    def win_coin(self):
        return self.coin * self.rate

    @property
    def decorated_coin(self):
        return self.__output.paint_yellow(self.__zero_filled_coin)

    @property
    def __zero_filled_coin(self):
        return str(self.coin).zfill(2)


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


class CasinoGame:
    HUMAN_PLAYRES = ['MY']
    COMPUTER_PLAYRES = ['C1', 'C2', 'C3']
    CELL_SIZE = 8

    def __init__(self):
        self.__players_dict = {}
        self.__cells_dict = {}
        self.__bets = []

    def play(self):
        self.__initialize()
        self.__show_coin()
        while not self.__is_game_end:
            self.__play_once()

    def __initialize(self):
        self.__create_cells()
        self.__create_players()

    def __show_coin(self):
        message = '[持ちコイン] '
        for player in self.__players:
            message += player.info
        print(message)

    def __play_once(self):
        self.__reset_bets()
        self.__bet_players()
        self.__show_table()
        self.__check_hit()
        self.__show_coin()

    def __find_bets(self, hit_cell):
        bets = []
        for bet in self.__bets:
            if bet.cell_name == hit_cell.name:
                bets.append(bet)
        return bets

    def __create_cells(self):
        for name in ['R', 'B']:
            self.__cells_dict[name] = TextCell(name, 2)

        for num in list(range(1, 9)):
            self.__cells_dict[str(num)] = NumberCell(str(num), self.CELL_SIZE)

    def __create_players(self):
        for name in self.HUMAN_PLAYRES:
            self.__players_dict[name] = Human(name, 500)
        for name in self.COMPUTER_PLAYRES:
            self.__players_dict[name] = Computer(name, 500)

    def __bet_players(self):
        for player in self.__players:
            self.__bets.append(player.get_bet(self.__cells_dict))

    def __check_hit(self):
        roulette = Roulette(self.__cells_dict)
        hit_cells = roulette.get_hit_cells()

        for hit_cell in hit_cells:
            hit_bets = self.__find_bets(hit_cell)
            for bet in hit_bets:
                player = self.__players_dict[bet.player_name]
                player.win(bet)

    def __reset_bets(self):
        self.__bets = []

    def __show_table(self):
        table = Table(self.__cells, self.__players, self.__bets)
        table.show()

    @property
    def __is_game_end(self):
        for player in self.__players:
            if player.is_bankruptcy:
                print(player.name + 'のコインがなくなったためゲームを終了します。')
                return True
        return False

    @property
    def __players(self):
        return list(self.__players_dict.values())

    @property
    def __cells(self):
        return list(self.__cells_dict.values())


casino = CasinoGame()
casino.play()
