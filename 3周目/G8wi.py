import random

teams = []


class Team:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense


def create_teams():
    global teams
    team1 = Team('アタッカーズ', 80, 20)
    team2 = Team('ディフェンダーズ', 30, 70)
    team3 = Team('アベレージーズ', 50, 50)
    teams = [team1, team2, team3]


def play():
    print('デバッグログ：play()')
    create_teams()


play()
