class Hand:

    hand: list[tuple[str]]

    def __init__(self, deck):
        self.hand = [deck.pop() for _ in range(2)]

    def __getitem__(self, index):
        return self.hand[index]

    def __int__(self):
        total = 0
        for element in self.hand:
            if element[1] in ["Jack", "Queen", "King"]:
                total += 10
            elif element[1] == "Ace":
                total += 11
            else:
                total += int(element[1])
        if total > 21:
            for element in self.hand:
                if element[1] == "Ace":
                    total -= 10
        return total

    def draw_card(self, deck: list[tuple[str]]) -> None:
        self.hand.append(deck.pop())


class Player(Hand):

    second_hand: list[tuple[str]]
    fiches: int

    def __init__(self, deck: list[tuple[str]]):
        super().__init__(deck)
        self.fiches = 100

    def split_hand(self, deck: list[tuple[str]]) -> list[tuple[str]]:
        second_hand = [self.hand.pop()]
        self.hand.append(deck.pop())
        second_hand.append(deck.pop())
        return second_hand

    def bet(self, amount: int) -> None:
        self.fiches -= amount

    def win(self, amount: int) -> None:
        self.fiches += amount * 2


class Dealer(Hand):

    def __init__(self, deck: list[tuple[str]]):
        super().__init__(deck)