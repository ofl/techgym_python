import random
import math


class Team:
    def __init__(self, name, attack, defense):
        self.name = name
        self.__attack = attack
        self.__defense = defense

    @classmethod
    def create(cls, name):
        attack = random.randint(20, 80)
        defense = 100 - attack
        return cls(name, attack, defense)

    def get_hit_rate(self):
        return random.randint(10, self.__attack)

    def get_out_rate(self):
        return random.randint(10, self.__defense)

    @property
    def info(self):
        return f"{self.__long_name}: 攻撃力:{str(self.__attack)} / 守備力:{str(self.__defense)}"

    @property
    def short_name(self):
        return self.name[0:2]

    @property
    def __long_name(self):
        return self.name.ljust(8, ' ')


class League:
    __TEAM_NAMES = ['Fighters', 'Giants', 'Dragons', 'Tigers', 'Carp', 'Hawks']

    def __init__(self):
        self.teams = self.__create_teams()

    def show_teams(self):
        print('全チームの情報')
        for i, team in enumerate(self.teams):
            print(f"{str(i + 1)}. {team.info}")

    def __create_teams(self):
        return list(map(Team.create, self.__TEAM_NAMES))


class Game:
    __TURNS_OF_INNING = ['先攻', '後攻']
    __DEFAULT_INNING_END = 9

    def __init__(self, league):
        self.__league = league
        self.__teams = []
        self.__innings = []

    def setup(self):
        if len(self.__teams) == 0:
            self.__select_teams()

    # 使用していない
    def set_teams(self, first_team, second_team):
        self.__teams.append(first_team)
        self.__teams.append(second_team)

    def play(self):
        for i in range(self.__DEFAULT_INNING_END):
            for j in self.__both_turns_of_inning:
                inning = self.__create_inning(i, j)
                inning.play()
                self.__innings.append(inning)

    def show_result(self):
        print(self.__scoreboard_header())
        for i in self.__both_turns_of_inning:
            print(self.__get_scoreboard(i))

    def __create_inning(self, num, turn):
        offensing_team = self.__teams[turn]
        defensing_team = self.__teams[int(not turn)]
        return Inning(num, turn, offensing_team.get_hit_rate(),
                      defensing_team.get_out_rate())

    def __select_teams(self):
        for i in self.__both_turns_of_inning:
            self.__select_team(i)

    def __select_team(self, turn):
        player_name = self.__TURNS_OF_INNING[turn]
        selected_number = int(
            input(player_name + 'のチームを選択してください（1〜3）'))
        selected_team = self.__league.teams[selected_number - 1]
        self.__teams.append(selected_team)
        print(player_name + 'のチームは「' + selected_team.name + '」です')

    def __scoreboard_header(self):
        return f"   | {' | '.join(self.__inning_numbers)} | R |"

    def __get_scoreboard(self, turn):
        scores = self.__get_inning_scores(turn)
        inning_scores = ' | '.join(list(map(str, scores)))
        team = self.__teams[turn]
        total_score = sum(scores)
        return ' | '.join([team.short_name, inning_scores, str(total_score)]) + ' | '

    def __get_inning_scores(self, turn):
        scores = []
        for inning in self.__innings:
            if inning.turn == turn:
                scores.append(inning.score)
        return scores

    @property
    def __inning_numbers(self):
        number_strings = []
        for inning in self.__innings:
            inning_num = str(inning.num + 1)
            if inning_num not in number_strings:
                number_strings.append(inning_num)
        return number_strings

    # イニングの表と裏(0または1の数字)
    @property
    def __both_turns_of_inning(self):
        return range(len(self.__TURNS_OF_INNING))


class Inning:
    def __init__(self, num, turn, hit_rate, out_rate):
        self.score = 0
        self.num = num  # 回
        self.turn = turn  # イニングの表裏(0: 表, 1: 裏)
        self.__hit_rate = hit_rate
        self.__out_rate = out_rate

    def play(self):
        inning_score = math.floor((self.__hit_rate - self.__out_rate) / 10)
        if inning_score < 0:
            inning_score = 0
        self.score = inning_score


if __name__ == '__main__':
    league = League()
    league.show_teams()
    game = Game(league)
    game.setup()
    game.play()
    game.show_result()
