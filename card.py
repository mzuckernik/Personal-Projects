class Card:
    """
    Blah blah blah
    """
    rank: str
    suit: str

    def __init__(self, rank: str, suit: str) -> None:
        """
        Class for cards in deck
        """
        self._rank = rank
        self._suit = suit

    @property
    def rank(self) -> str:
        return self._rank
    
    @property
    def suit(self) -> str:
        return self._suit
    
    def __str__(self) -> str:
        return self.rank + self.suit