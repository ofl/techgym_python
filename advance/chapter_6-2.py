import requests
import cv2 as cv
import os
import matplotlib.pyplot as plt
import numpy as np
import random


class Card:
    def __init__(self, mark, display_name, image):
        self.mark = mark
        self.display_name = display_name
        self.image = image
        self.is_dealt = False

    def numbers(self):
        if self.display_name == 'A':
            return [1, 11]
        elif self.display_name in ['J', 'Q', 'K']:
            return [10]
        else:
            return [int(self.display_name)]


class CardImageSet:
    def __init__(self):
        self.card_images = []
        self.__load_image()

    def __load_image(self):
        image_name = 'cards.jpg'
        vsplit_number = 4
        hsplit_number = 13

        if not os.path.isfile(image_name):
            response = requests.get(
                'http://3156.bz/techgym/cards.jpg', allow_redirects=False)
            with open(image_name, 'wb') as image:
                image.write(response.content)

        img = cv.imread('./'+image_name)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        h, w = img.shape[:2]
        crop_img = img[:h // vsplit_number * vsplit_number,
                       :w // hsplit_number * hsplit_number]

        self.card_images.clear()
        for h_image in np.vsplit(crop_img, vsplit_number):
            for v_image in np.hsplit(h_image, hsplit_number):
                self.card_images.append(v_image)


class CardSet:
    MARKS = ['ハート', 'スペード', 'ダイヤ', 'クローバー']
    DISPLAY_NAMES = ['A', '2', '3', '4', '5',
                     '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, image_set=CardImageSet()):
        self.__cards = []
        self.__create_cards(image_set.card_images)

    def hit(self):
        tmp_cards = list(filter(lambda n: n.is_dealt == False, self.__cards))
        assert (len(tmp_cards) != 0), "残りカードなし"

        tmp_card = random.choice(tmp_cards)
        tmp_card.is_dealt = True
        return tmp_card

    def __create_cards(self, card_images):
        self.__cards.clear()
        size = len(self.DISPLAY_NAMES)
        for i, mark in enumerate(self.MARKS):
            for j in range(size):
                self.__cards.append(
                    Card(mark, self.DISPLAY_NAMES[j], card_images[i*size+j]))


class CardPlotter:
    @staticmethod
    def show_cards(cards):
        for i, card in enumerate(cards):
            print(f"{card.mark}{card.display_name}")
            plt.subplot(1, 6, i + 1)
            plt.axis('off')
            plt.imshow(card.image)
        plt.show()


class Player:
    def __init__(self, name):
        self.name = name
        self.cards_in_hand = None


class Human(Player):
    def __init__(self):
        super().__init__('自分')

    def hit_or_stand(self, card_set):
        while True:
            if self.__stop_hitting():
                break
            else:
                self.cards_in_hand.hit_from(card_set)
                self.cards_in_hand.show()

    def __stop_hitting(self):
        if self.cards_in_hand.is_burst():
            return True

        message = 'ヒット[1] or スタンド[2]'
        choice_key = input(message)
        while not enable_choice(choice_key):
            choice_key = input(message)
        return int(choice_key) == 2


class Computer(Player):
    def __init__(self):
        super().__init__('コンピューター')

    def hit_or_stand(self, card_set):
        while True:
            if self.__stop_hitting():
                break
            else:
                self.cards_in_hand.hit_from(card_set)

    def __stop_hitting(self):
        if self.cards_in_hand.is_burst():
            return True

        return self.cards_in_hand.is_blackjack() or self.cards_in_hand.min_total_number() >= 18


class PlayerCardsInHand:
    def __init__(self, plotter_class=CardPlotter):
        self.cards = []
        self.__total_numbers = [0]
        self.plotter_class = plotter_class

    def show(self):
        self.plotter_class.show_cards(self.cards)

    def hit_from(self, card_set):
        self.cards.append(card_set.hit())
        self.__update_total_numbers()

    def is_blackjack(self):
        return BLACK_JACK in self.__total_numbers

    def is_burst(self):
        return self.min_total_number() > BLACK_JACK

    def number_for_judge(self):
        not_burst_numbers = list(
            filter(lambda n: n < BLACK_JACK, self.__total_numbers))

        if len(not_burst_numbers) > 0:
            return max(not_burst_numbers)
        else:
            return self.min_total_number()

    def min_total_number(self):
        return min(self.__total_numbers)

    def __update_total_numbers(self):
        totals = [0]
        for card in self.cards:
            l = []
            for number in card.numbers():
                for total in totals:
                    l.append(total + number)
            totals = l
        self.__total_numbers = totals


def enable_choice(string):
    if not string.isdigit():
        return False

    return 1 <= int(string) <= 2


class BlackJack:
    def __init__(self, players):
        self.players = players
        self.card_set = CardSet()
        for player in players:
            player.cards_in_hand = PlayerCardsInHand()

    def play(self):
        player = self.players[0]
        dealer = self.players[1]

        player.cards_in_hand.hit_from(self.card_set)
        dealer.cards_in_hand.hit_from(self.card_set)
        player.cards_in_hand.hit_from(self.card_set)
        dealer.cards_in_hand.hit_from(self.card_set)

        player.cards_in_hand.show()

        player.hit_or_stand(self.card_set)
        dealer.hit_or_stand(self.card_set)

        winner = self.__get_winner()
        self.__show_result(winner)

    def __show_result(self, winner):
        for player in self.players:
            print(f"{player.name}のカードは")
            player.cards_in_hand.show()

        if winner is None:
            print('引き分け')
        else:
            print(f"{winner.name}の勝ち")

    def __get_winner(self):
        player = self.players[0]
        dealer = self.players[1]

        player_is_burst = player.cards_in_hand.is_burst()
        dealer_is_burst = dealer.cards_in_hand.is_burst()

        if player_is_burst and dealer_is_burst:
            return None
        elif dealer_is_burst:
            return player
        elif player_is_burst:
            return dealer

        player_total = player.cards_in_hand.number_for_judge()
        dealer_total = dealer.cards_in_hand.number_for_judge()

        if player_total == dealer_total:
            return None
        elif player_total > dealer_total:
            return player
        else:
            return dealer


class Game:
    def __init__(self, players, game_class):
        self.players = players
        self.game_class = game_class

    def play(self):
        game = self.game_class(self.players)
        game.play()


if __name__ == "__main__":
    BLACK_JACK = 21

    players = []
    players.append(Human())
    players.append(Computer())

    game = Game(players, BlackJack)
    game.play()
