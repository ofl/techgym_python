import random
import math

teams = []
playing_teams = {'myself': None, 'enemy': None}
inning_type = {'front': '表', 'back': '裏'}
innings = []


class Team:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.scores = []
        self.total_score = 0

    def info(self):
        print(self.name + ': 攻撃力:' + str(self.attack) +
              ' / 守備力:' + str(self.defense))

    def get_hit_rate(self):
        return random.randint(10, self.attack)

    def get_out_rate(self):
        return random.randint(10, self.defense)

    @property
    def scoreboard(self):
        return ' | '.join(self.scores)


def create_teams():
    global teams
    team1 = Team('アタッカーズ', 80, 20)
    team2 = Team('ディフェンダーズ', 30, 70)
    team3 = Team('アベレージーズ', 50, 50)
    teams = [team1, team2, team3]


def show_teams():
    index = 1
    print('全チームの情報')
    for team in teams:
        print(str(index))
        team.info()
        index += 1


def choice_team(player):
    if player == 'myself':
        player_name = '自分'
    elif player == 'enemy':
        player_name = '相手'

    choice_team_number = int(input(player_name + 'のチームを選択してください（1〜3）'))
    playing_teams[player] = teams[choice_team_number - 1]
    print(player_name + 'のチームは「' + playing_teams[player].name + '」です')


def get_play_inning(inning):
    if inning == 'front':
        offence = 'myself'
        defense = 'enemy'
    else:
        defense = 'myself'
        offence = 'enemy'

    hit_rate = playing_teams[offence].get_hit_rate()
    out_rate = playing_teams[defense].get_out_rate()
    inning_score = math.floor((hit_rate - out_rate) / 10)
    if inning_score < 0:
        inning_score = 0
    playing_teams[offence].total_score += inning_score
    playing_teams[offence].scores.append(str(inning_score))
    return inning_score


def play():
    create_teams()
    show_teams()
    choice_team('myself')
    choice_team('enemy')
    for i in range(9):
        innings.append(str(i))
        for j in range(2):
            inning = ('front' if j % 2 == 0 else 'back')
            get_play_inning(inning)
    my_team = playing_teams['myself']
    enemy_team = playing_teams['enemy']

    print(f"　　| {' | '.join(innings)} | R |")
    print(f"自分| {my_team.scoreboard} | {str(my_team.total_score)} |")
    print(f"相手| {enemy_team.scoreboard} | {str(enemy_team.total_score)} |")


play()
