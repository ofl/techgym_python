import random
import math


class Team:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.scores = []

    @classmethod
    def create(cls, name):
        attack = random.randint(20, 80)
        defense = 100 - attack
        return cls(name, attack, defense)

    def get_hit_rate(self):
        return random.randint(10, self.attack)

    def get_out_rate(self):
        return random.randint(10, self.defense)

    def reset_score(self):
        self.scores = []

    @property
    def info(self):
        return f"{self.__long_name}: 攻撃力:{str(self.attack)} / 守備力:{str(self.defense)}"

    @property
    def total_score(self):
        return sum(self.scores)

    @property
    def scoreboard(self):
        inning_scores = ' | '.join(list(map(str, self.scores)))
        return ' | '.join([self.__short_name, inning_scores, str(self.total_score)]) + ' | '

    @property
    def __long_name(self):
        return self.name.ljust(8, ' ')

    @property
    def __short_name(self):
        return self.name[0:2]


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
    __MATCH_ORDER = ['先攻', '後攻']

    def __init__(self, first_team=None, second_team=None):
        self.__league = League()
        self.__teams = []
        self.__innings = []
        self.__is_top_of_inning = True  # イニングの表かどうか？

        if first_team:
            self.__teams.append(first_team)
        if second_team:
            self.__teams.append(second_team)

    def setup(self):
        self.__league.show_teams()
        if len(self.__teams) == 0:
            self.__select_teams()
        self.__reset_scores()

    def play(self):
        for i in range(9):
            self.__innings.append(str(i + 1))
            for j in range(2):
                self.__is_top_of_inning = bool(j)
                self.__play_inning()

    def show_result(self):
        print(self.__scoreboard_header())
        for i in range(len(self.__MATCH_ORDER)):
            print(self.__teams[i].scoreboard)

    def __select_teams(self):
        for i in range(len(self.__MATCH_ORDER)):
            self.__select_team(i)

    def __reset_scores(self):
        for team in self.__teams:
            team.reset_score()

    def __select_team(self, index):
        player_name = self.__MATCH_ORDER[index]
        selected_number = int(
            input(player_name + 'のチームを選択してください（1〜3）'))
        selected_team = self.__league.teams[selected_number - 1]
        self.__teams.append(selected_team)
        print(player_name + 'のチームは「' + selected_team.name + '」です')

    def __play_inning(self):
        self.__offensing_team.scores.append(self.__get_inning_score())

    def __get_inning_score(self):
        hit_rate = self.__offensing_team.get_hit_rate()
        out_rate = self.__defensing_team.get_out_rate()
        inning_score = math.floor((hit_rate - out_rate) / 10)
        if inning_score < 0:
            inning_score = 0
        return inning_score

    def __scoreboard_header(self):
        return f"   | {' | '.join(self.__innings)} | R |"

    @property
    def __offensing_team(self):
        return self.__teams[bool(self.__is_top_of_inning)]

    @property
    def __defensing_team(self):
        return self.__teams[bool(not self.__is_top_of_inning)]


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.play()
    game.show_result()
