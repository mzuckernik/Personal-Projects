import random
import emoji
from best_hand import best_hand

# Define suits and ranks
suits = [emoji.emojize(':heart_suit:'), emoji.emojize(':diamond_suit:'), emoji.emojize(':club_suit:'), emoji.emojize(':spade_suit:')]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def create_deck():
    """Creates a standard deck of 52 cards."""
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

def shuffle_deck(deck):
    """Shuffles the deck."""
    random.shuffle(deck)

def deal_cards(deck, num_players, cards_per_player):
    """Deals cards to players."""
    hands = {f"Player {i + 1}": [] for i in range(num_players)}
    for _ in range(cards_per_player):
        for player in hands:
            if deck:  # Ensure there are still cards to deal
                hands[player].append(deck.pop(0))
    return hands

def display_hands(hands):
    """Displays each player's hand."""
    for player, cards in hands.items():
        print(f"{player}'s hand: {', '.join(cards)}")

def main():
    print("Welcome to a 4-player Poker Game!")
    
    # Create and shuffle the deck
    deck = create_deck()
    shuffle_deck(deck)

    # Deal 2 cards per player (Texas Hold'em style)
    num_players = 4
    cards_per_player = 2
    hands = deal_cards(deck, num_players, cards_per_player)

    # Display players' hands
    display_hands(hands)

    # Deal community cards (flop, turn, river)
    community_cards = []
    for i, stage in enumerate(["Flop", "Turn", "River"], 1):
        if stage == "Flop":
            community_cards.extend([deck.pop(0) for _ in range(3)])  # 3 cards for the flop
        else:
            community_cards.append(deck.pop(0))  # 1 card for turn and river
        print(f"{stage}: {', '.join(community_cards)}")
    return best_hand(hands, community_cards)

if __name__ == "__main__":
    main()
