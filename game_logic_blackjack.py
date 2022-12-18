import itertools
import random


class Hand:

    first_hand: list[tuple[str]]
    second_hand: list[tuple[str]]

    def __init__(self, deck):
        self.first_hand = [deck.pop() for _ in range(2)]
        self.second_hand = []

    def __getitem__(self, index):
        return self.first_hand[index]

    def __int__(self):
        total = 0
        for element in self.first_hand:
            if element[1] in ["Jack", "Queen", "King"]:
                total += 10
            elif element[1] == "Ace":
                total += 11
            else:
                total += int(element[1])
        if total > 21:
            for element in self.first_hand:
                if element[1] == "Ace":
                    total -= 10
        return total

    def get_cards(self):
        return str(self.first_hand), str(self.second_hand)

    def draw_card(self, deck: list[tuple[str]]) -> None:
        self.first_hand.append(deck.pop())

    def split_hand(self, deck: list[tuple[str]]) -> list[tuple[str]]:
        splitted = True
        second_hand = [self.first_hand.pop()]
        self.first_hand.append(deck.pop())
        second_hand.append(deck.pop())
        return splitted, second_hand

    def check_hand_sum(self) -> str:
        total = int(self)
        if total == 21:
            return "Blackjack"
        elif total > 21:
            return "Bust"


class Player:

    hand: Hand
    fiches: int

    def __init__(self, deck: list[tuple[str]]):
        self.hand = Hand(deck)
        self.fiches = 100

    def __str__(self):
        return f'Hand: {str(self.hand)}\nFiches: {self.fiches}'

    def __int__(self):
        return self.fiches

    def bet(self, amount: int) -> None:
        self.fiches -= amount

    def win(self, amount: int) -> None:
        self.fiches += amount * 2


class Dealer:

    hand: Hand

    def __init__(self, deck: list[tuple[str]]):
        self.hand = Hand(deck)

    def __str__(self):
        return f'Hand: {str(self.hand)}'

    def __int__(self):
        return int(self.hand)

    def draw_card(self, deck: list[tuple[str]]) -> None:
        self.hand.draw_card(deck)

    def check_hand_sum(self) -> str:
        return self.hand.check_hand_sum()


SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8",
         "9", "10", "Jack", "Queen", "King", "Ace"]


def create_deck() -> list[tuple[str]]:
    deck = list(itertools.product(SUITS, RANKS))
    deck += deck
    random.shuffle(deck)
    return deck


deck = create_deck()
player = Player(deck)
dealer_hand = Hand(deck)
