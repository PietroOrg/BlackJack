import itertools
import random

SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8",
         "9", "10", "Jack", "Queen", "King", "Ace"]


class Hand:

    first_hand: list[tuple[str]]
    second_hand: list[tuple[str]]

    def __init__(self, deck):
        self.first_hand = [deck.pop() for _ in range(2)]

    def __str__(self):
        return str(self.first_hand), str(self.second_hand) if self.second_hand else str(self.first_hand)

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

    hand:

    def __init__(self, deck):
        hand = Hand(deck)


''' controlla chi ha vinto tra il giocatore e il banco
def check_winner(dealer_hand, player_hand):
    if hand_sum(dealer_hand) > hand_sum(player_hand) and check_hand_sum(dealer_hand) != "Bust":
        print("Dealer wins")
    elif hand_sum(dealer_hand) < hand_sum(player_hand) and check_hand_sum(player_hand) != "Bust":
        print("Player wins")
    else:
        print("Draw")
'''


''' controlla la somma delle carte in mano del dealer
def dealer_draws(deck, dealer_hand, first_hand, second_hand):
    # controlla se il delaer deve pescare una carta per vincere
    if (
            (check_hand_sum(first_hand) not in ["Blackjack", "Bust"] or
             check_hand_sum(second_hand) not in ["Blackjack", "Bust"]) and
            check_hand_sum(dealer_hand) not in ["Blackjack", "Bust"] and
            (hand_sum(dealer_hand) < hand_sum(first_hand) or
             hand_sum(dealer_hand) < hand_sum(second_hand))
    ):
        print("Dealer draws a card")
        dealer_hand.append(deck.pop())
        print("Dealer hand: ", *dealer_hand)
        dealer_draws(deck, dealer_hand, first_hand, second_hand)
'''


'''chiede all'utente se vuole pescare o no
def player_draws(deck, hand, splitted):
    while check_hand_sum(hand) not in ["Blackjack", "Bust"]:
        if (hand[0][1] == hand[1][1] or (hand[0][1] in RANKS[8:13] and hand[1][1] in RANKS[8:13])) and not (splitted):
            choice = input("Hit/Stand/Double/Split: ").lower()
        else:
            choice = input("Hit/Stand/Double: ").lower()
        if choice in ["hit", "double"]:
            hand.append(deck.pop())
            print("Player hand: ", *hand)
        elif choice == "stand":
            print("Sum: ", hand_sum(hand))
            return
        elif choice == "split":
            return split_hand(hand, deck, player_draws)
'''


# crea un mazzo e lo riempe con 104 carte
def create_deck() -> list[tuple[str]]:
    deck = list(itertools.product(SUITS, RANKS))
    deck += deck
    random.shuffle(deck)
    return deck


def main() -> None:
    splitted = False
    deck = create_deck()
    player_hand = Hand(deck)
    dealer_hand = Hand(deck)
    print(f'Player hand: {player_hand}')
    print(f'Dealer hand: [{dealer_hand[0]}, ("X", "X")]')

    if dealer_hand.check_hand_sum() == 'Blackjack':
        print(f'Dealer hand: {dealer_hand}')
        print("Dealer wins")
        return
    if player_hand.check_hand_sum() == 'Blackjack':
        print(f'Dealer hand: {dealer_hand}')
        print("Player wins")
        return

    '''
    if check_hand_sum(dealer_hand) != "Blackjack":
        splitted = player_draws(deck, player_hand, splitted)
        print("Dealer hand: ", *dealer_hand)
        player_second_hand = []
        dealer_draws(deck, dealer_hand, player_hand, player_second_hand)
        # controlla chi ha vinto
        if splitted:
            print("First hand: ", end="")
            check_winner(dealer_hand, player_hand)
            print("Second hand: ", end="")
            check_winner(dealer_hand, player_second_hand)
        else:
            check_winner(dealer_hand, player_hand)
    else:
        print("Dealer hand: ", *dealer_hand)
        print("Dealer wins")
    '''


if __name__ == "__main__":
    main()
