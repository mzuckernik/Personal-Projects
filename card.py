from collections import Counter
import emoji
from typing import Optional

H = emoji.emojize(':heart_suit:')
D = emoji.emojize(':diamond_suit:')
C = emoji.emojize(':club_suit:')
S = emoji.emojize(':spade_suit:')

RANK_ORDER = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "T": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }
rank_order = "23456789TJQKA"


def is_sequential(lst: list[int]) -> bool:
        """
        Checks if each element is exactly 1 greater than the previous element
        """
        for i in range(1, len(lst)):
            if lst[i] != lst[i - 1] + 1:
                return False
        return True


class Card:
    """
    Class for cards in deck
    """
    rank: str
    suit: str

    def __init__(self, rank: str, suit: str) -> None:
        """
        Initializes card
        """
        self._rank = rank
        self._suit = suit
        if self._suit == H or self._suit == D:
            self.color = "\033[0;31m"
        else:
            self.color = "\033[0m"

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def suit(self) -> str:
        return self._suit
    
    def __repr__(self) -> str:
        return self.color + self._rank + self._suit + "\033[0m"
    
class Hand:
    """
    Class for poker hands containing between 5 and 7 Cards
    """
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def __len__(self):
        return len(self.cards)
    
    def rm(self, card: Card) -> None:
        self.cards.remove(card)

    def spare(self, suit: str) -> None:
        """
        Remove cards of all suits except for the input
        """
        self.cards = [card for card in self.cards if card.suit == suit]

    def __repr__(self) -> str:
        return ', '.join(str(card) for card in self.cards)
    
    def suits(self) -> list[str]:
        return [card._suit for card in self.cards]

    def ranks(self) -> list[str]:
        return [card._rank for card in self.cards]

    @property
    def suit_counter(self) -> Counter:
        return Counter(self.suits())
    
    def flush_type(self) -> Optional[tuple[str, int]]:
        for suit in self.suit_counter:
            if self.suit_counter[suit] >= 5:
                return suit, self.suit_counter[suit]
        return '', 0
    
    def best_straight(self) -> tuple[bool, list[int]]:
        """
        sorted(set([RANK_ORDER[rank] for rank in ranks]))
        """
        ranks: list[int] = sorted(set([RANK_ORDER[rank] for rank in self.ranks()]))

        # A straight cannot exist without 5 distinct ranks
        if len(ranks) < 5:
            return False

        # Ace can act as 1 for the low straight
        if 14 in ranks:
            ranks.insert(0, 1)

        # Determine the best straight
        best_straight = []
        for i in range(len(ranks) - 4):
            potential = ranks[i:i+5]
            # If potential is a straight
            if is_sequential(potential) and potential > best_straight:
                    best_straight = potential

        if len(best_straight) != 0:
            reverse_rank_order = {v: k for k, v in RANK_ORDER.items()}
            best_straight_str = ['A' if val == 1 else reverse_rank_order[val] for val in best_straight]
            return True, best_straight_str

        return False, best_straight
    
    def is_straight(self) -> bool:
        """
        Checks if ranks form a consecutive sequence.
        """
        indices = sorted(rank_order.index(rank) for rank in self.ranks())
        return indices == list(range(indices[0], indices[0] + 5)) or indices == [0, 1, 2, 3, 12]
    

    def sort_ranks(self) -> int:
        rank_counter = Counter(self.ranks())
        sorted_ranks = sorted(rank_counter.items(), key=lambda x: (-x[1], -rank_order.index(x[0])))



    def hand_strength(self) -> tuple[int, Optional[list[str]]]:
        has_straight, best = self.best_straight()
        suit, num_of_same_suit = self.flush_type()
        # The flush is the strongest hand
        if num_of_same_suit == 5:
            self.spare(suit)
            if self.is_straight():
                return ()
