'''
3章の改良
Inningのデータをリストで持つように変更したりScoreBoardの導入などクラスの責務を整理した
'''

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

    @property
    def hit_rate(self):
        return random.randint(10, self.__attack)

    @property
    def out_rate(self):
        return random.randint(10, self.__defense)

    @property
    def info(self):
        return f"{self.__formatted_name}: 攻撃力:{str(self.__attack)} / 守備力:{str(self.__defense)}"

    @property
    def short_name(self):
        return self.name[0:2]

    @property
    def __formatted_name(self):
        return self.name.ljust(8, ' ')


class League:
    __TEAM_NAMES = ['Fighters', 'Giants', 'Dragons', 'Tigers', 'Carp', 'Hawks']

    def __init__(self):
        self.teams = self.__create_teams()

    def show_teams(self):
        print('全チームの情報')
        for i, team in enumerate(self.teams):
            print(f"{str(i + 1)}. {team.info}")

    def select_team(self, turn):
        selected_number = int(
            input(turn + f'のチームを選択してください（1〜{len(self.__TEAM_NAMES)}）'))
        selected_team = self.teams[selected_number - 1]
        print(turn + 'のチームは「' + selected_team.name + '」です')
        return selected_team

    def __create_teams(self):
        return list(map(Team.create, self.__TEAM_NAMES))


class BaseBall:
    __DEFAULT_INNING_END = 9

    def __init__(self, teams):
        self.__teams = teams
        self.innings = []

    def play(self):
        first_team_score = 0
        last_team_score = 0

        while True:
            inning = Inning(self.__teams)
            inning.play()

            first_team_score += inning.scores[0]
            last_team_score += inning.scores[1]

            self.innings.append(inning)
            if self.__is_game_over(first_team_score, last_team_score):
                break

    def __is_game_over(self, first_team_score, last_team_score):
        if len(self.innings) < self.__DEFAULT_INNING_END:
            return False

        return not first_team_score == last_team_score


class Inning:
    def __init__(self, teams):
        self.scores = []
        self.__teams = teams

    def play(self):
        for i in range(len(self.__teams)):
            first_team = self.__teams[i % 2]
            last_team = self.__teams[(i + 1) % 2]
            score = self.get_score(
                first_team.hit_rate, last_team.out_rate)
            self.scores.append(score)

    @ staticmethod
    def get_score(hit_rate, out_rate):
        inning_score = math.floor((hit_rate - out_rate) / 10)
        if inning_score < 0:
            inning_score = 0
        return inning_score


class ScoreBoard:
    def __init__(self, teams, innings):
        self.__teams = teams
        self.__innings = innings

    def show(self):
        print(self.__scoreboard_header())
        for i in range(2):
            scores = list(map(lambda k: k.scores[i], self.__innings))
            print(self.__get_scoreboard(self.__teams[i], scores))

    def __scoreboard_header(self):
        inning_nums = list(range(1, self.__inning_count + 1))
        return f"   | {' | '.join(list(map(str, inning_nums)))} | R |"

    def __get_scoreboard(self, team, scores):
        inning_scores = ' | '.join(list(map(str, scores)))
        total_score = sum(scores)
        return ' | '.join([team.short_name, inning_scores, str(total_score)]) + ' | '

    @ property
    def __inning_count(self):
        return len(self.__innings)


if __name__ == '__main__':
    league = League()
    league.show_teams()
    playing_teams = [league.select_team('先攻'), league.select_team('後攻')]

    game = BaseBall(playing_teams)
    game.play()

    scoreboard = ScoreBoard(playing_teams, game.innings)
    scoreboard.show()
