import ast
import random

def first_play(six_six):
    for player, hand in six_six.items():
        if (6, 6) in hand:
            return player
    return None


def _available_sides(piece, table):
    if not table:
        return []

    a, b = piece
    left_open = table[0][0]
    right_open = table[-1][1]
    sides = []

    if a == left_open or b == left_open:
        sides.append("left")
    if a == right_open or b == right_open:
        sides.append("right")
    return sides


def table_is_valid(piece, table, side=None):
    if not table:
        return True

    sides = _available_sides(piece, table)
    if side is None:
        return bool(sides)
    return side in sides


def play_piece(hand, piece, side, table):
    if piece not in hand or not table_is_valid(piece, table, side):
        return False

    a, b = piece

    if not table:
        table.append((a, b))
    elif side == "left":
        left_open = table[0][0]
        if b == left_open:
            table.insert(0, (a, b))
        else:
            table.insert(0, (b, a))
    elif side == "right":
        right_open = table[-1][1]
        if a == right_open:
            table.append((a, b))
        else:
            table.append((b, a))
    else:
        return False

    hand.remove(piece)
    return True


def _read_piece(value):
    try:
        piece = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return None

    if isinstance(piece, list):
        piece = tuple(piece)

    if (
        isinstance(piece, tuple)
        and len(piece) == 2
        and all(type(value) is int for value in piece)
    ):
        return piece
    return None


def play_turn(players, hand, table, buyable_pile, opponent_name, opponent_hand):
    legal_pieces = [piece for piece in hand if table_is_valid(piece, table)]
    if players != "bot1":
        # Traz as informações necessárias para o jogador tomar as decisões
        print(f"\n{players}'s turn")
        print(f"Your hand: {hand}")
        print(f"Table: {table}")
        print(f"{opponent_name} has {len(opponent_hand)} pieces")
        
        if not legal_pieces:
            print(f"{players} has no playable piece and must buy")

    if players != "bot1":
        print(f"Playable pieces: {legal_pieces}")

    while True:
        choice = input("Choose a piece like (2, 5) or buy: ").strip()
        if choice.lower() == "buy":
            if legal_pieces:
                print("You have playable pieces and cannot buy.")
                continue
        if choice.lower() == "buy":
            if not legal_pieces:
                if not buyable_pile:
                    print("There are no pieces left to buy.")
                    return False
            piece = buyable_pile.pop()
            hand.append(piece)
            print(f"{players} bought {piece}.")
            print(f"Your hand: {hand}")
            legal_pieces = [piece for piece in hand if table_is_valid(piece, table)]
            if legal_pieces:
                print(f"Playable pieces: {legal_pieces}")
            else:
                print("The bought piece is not playable.")
            continue

        piece = _read_piece(choice)
        if piece is None:
            print("Invalid format. Enter a piece like (2, 5).")
            continue
        if piece not in hand:
            print("That piece is not in your hand.")
            continue

        sides = _available_sides(piece, table)
        if table and not sides:
            print("That piece does not match either open end.")
            continue

        if len(sides) == 2:
            while True:
                end = input("It fits both ends. Choose 'left' or 'right': ").strip().lower()
                aliases = {"l": "left", "left": "left", "r": "right", "right": "right"}
                side = aliases.get(end)
                if side in sides:
                    break
                print("Please enter 'left' or 'right'.")
        elif sides:
            side = sides[0]
        else:
            # Any piece can start an empty table; its tuple order sets the ends.
            side = None

        if play_piece(hand, piece, side, table):
            print(f"{players} played {piece} on the {side or 'table'}.")
            print(f"Table is now: {table}")
            return True

        print("That move could not be made. Choose another piece or pass.")

def pass_turn(current_player, players):
    """Return the next player's name, wrapping from the last player to the first."""
    if not players:
        return None
    if current_player not in players:
        raise ValueError(f"Unknown player: {current_player}")

    current_index = players.index(current_player)
    next_index = (current_index + 1) % len(players)
    return players[next_index]


def opponent_play(hand, table):
    legal_pieces = [piece for piece in hand if table_is_valid(piece, table)]
    if not legal_pieces:
        print("bot1 has no playable piece and must pass.")
        return False
    piece = random.choice(legal_pieces)
    sides = _available_sides(piece, table)
    side = random.choice(sides) if sides else None

    if not play_piece(hand, piece, side, table):
        raise RuntimeError(f"bot1 could not play its selected piece: {piece}")

    print(f"bot1 played {piece} on the {side or 'table'}.")
    print(f"Table is now: {table}")
    return True

def sum_hands(hand):
    """Return each player's hand total, or a single hand's total."""
    if isinstance(hand, dict):
        scores = {player: sum(sum(piece) for piece in pieces) for player, pieces in hand.items()}
        if scores:
            lowest_score = min(scores.values())
            lowest_players = [player for player, score in scores.items() if score == lowest_score]
            print(f"Jogador(es) com a menor pontuação: {', '.join(lowest_players)} ({lowest_score} pontos)")
        return scores
    return sum(sum(piece) for piece in hand)