import random


class Team:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense


def play():
    print('デバッグログ：play()')


def create_teams():
    global teams
    team1 = Team('アタッカーズ', 80, 20)
    team2 = Team('ディフェンダーズ', 30, 70)
    team3 = Team('アベレージーズ', 50, 50)
    teams.append(team1)
    teams.append(team2)
    teams.append(team3)


teams = []
play()
