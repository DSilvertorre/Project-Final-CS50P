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
def generate_hands(shuffled_pieces):
    new_round_hands = []
    for p in range(4):
        hand = shuffled_pieces[p * 6:(p + 1) * 6]
        new_round_hands.append(hand)
    return new_round_hands


