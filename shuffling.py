import random
import itertools

# Definindo todas as pedras possíveis do dominó
def all_domino_pieces():
    all_oombinations = list(itertools.combinations_with_replacement(range(0, 7), 2))
    return all_oombinations

# Embaralha toda as peças do domino
def shuffle_pieces(all_combinations):
    new_round = all_combinations.copy()
    random.shuffle(new_round)
    return new_round

# Gera as mãos de cada jogador
def generate_hands(shuffled_pieces, number_of_players=4):
    new_round_hands = []
    for p in range(number_of_players):
        hand = shuffled_pieces[p * 7:(p + 1) * 7]
        new_round_hands.append(hand)
    return new_round_hands

def buyable_pieces(shuffled_pieces, hands_players):
    dealt_pieces = {piece for hand in hands_players for piece in hand}
    return [piece for piece in shuffled_pieces if piece not in dealt_pieces]