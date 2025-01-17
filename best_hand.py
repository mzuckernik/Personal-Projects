from collections import Counter
import emoji
from itertools import combinations
from card import Card

HAND_RANKS = ["High Card", "One Pair", "Two Pair", "Three of a Kind", 
              "Straight", "Flush", "Full House", "Four of a Kind", 
              "Straight Flush", "Royal Flush"]
H = emoji.emojize(':heart_suit:')
D = emoji.emojize(':diamond_suit:')
C = emoji.emojize(':club_suit:')
S = emoji.emojize(':spade_suit:')
RANK_ORDER = "23456789TJQKA"

# Helper functions
def is_flush(suits: list[str]) -> bool:
    """Checks if all cards are of the same suit."""
    return len(set(suits)) == 1

def is_straight(ranks: list[str]) -> bool:
    """Checks if ranks form a consecutive sequence."""
    indices = sorted(RANK_ORDER.index(rank) for rank in ranks)
    return indices == list(range(indices[0], indices[0] + 5)) or indices == [0, 1, 2, 3, 12]

def hand_rank(cards: list[Card]) -> tuple[int, list]:
    """Determines the rank of a poker hand."""
    suits: list[str] = [card._suit for card in cards]
    ranks: list[str] = [card._rank for card in cards]
    rank_values: list[str] = [RANK_ORDER.index(rank) for rank in ranks]

    # Sort ranks by frequency and value
    rank_counter = Counter(ranks)
    sorted_ranks = sorted(rank_counter.items(), key=lambda x: (-x[1], -RANK_ORDER.index(x[0])))

    # How many cards of the same ranks
    num_same = rank_counter.values()

    # Check for Flush and Straight
    flush = is_flush(suits)
    straight = is_straight(ranks)

    # Determine hand rank
    if flush and straight:
        return (9 if "T" in ranks and "A" in ranks else 8, rank_values)  # Royal or Straight Flush
    elif 4 in num_same:
        return (7, sorted_ranks)  # Four of a Kind
    elif 3 in num_same and 2 in num_same:
        return (6, sorted_ranks)  # Full House
    elif flush:
        return (5, rank_values)  # Flush
    elif straight:
        return (4, rank_values)  # Straight
    elif 3 in num_same:
        return (3, sorted_ranks)  # Three of a Kind
    elif list(num_same).count(2) == 2:
        return (2, sorted_ranks)  # Two Pair
    elif 2 in num_same:
        return (1, sorted_ranks)  # One Pair
    else:
        return (0, rank_values)  # High Card

def best_hand(player_hands: dict[str, list[Card]], community_cards: list[Card]) -> tuple[list[str], list[str], list[str]]:
    """Determines the best hand among players."""
    best_players = []
    bestest_combinations = []
    best_rank = (-1, [])

    for player, hand in player_hands.items():
        combined_cards: list[Card] = hand + community_cards
        best_combination = max((comb for comb in combinations(combined_cards, 5)), key=hand_rank)
        print(best_combination)
        current_rank = hand_rank(best_combination)

        if current_rank > best_rank:
            best_rank = current_rank
            best_players = [player]
            bestest_combinations = [best_combination]
        elif current_rank == best_rank:
            best_players.append(player)
            bestest_combinations.append(best_combination)

    return best_players, best_rank, bestest_combinations

def print_draw(players: list[str]) -> str:
    if len(players) == 2:
        return f"{players[0]} and {players[1]}"
    return ", ".join(players[:-1]) + f", and {players[-1]}"

# Example
if __name__ == "__main__":
    community_cards = [Card("5", S), Card("A", H), Card("T", H), Card("3", C), Card("A", C)]
    player_hands = {
        "Player 1": [Card("3", H), Card("K", D)], 
        "Player 2": [Card("3", D), Card("Q", D)]
    }

    winners, rank, hands = best_hand(player_hands, community_cards)
    if len(winners) == 1:
        print(f"The winner is {winners[0]} with a {HAND_RANKS[rank[0]]}: {hands[0]}")
    else:
        print(f"There was a draw between {print_draw(winners)} with a {HAND_RANKS[rank[0]]}")
    