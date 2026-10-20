from game import first_play, pass_turn, play_piece, play_turn, opponent_play, sum_hands
from shuffling import all_domino_pieces, buyable_pieces, generate_hands, shuffle_pieces

def username():
    player_main = input("Enter your nickname: ")
    bot1 = "bot1"
    return player_main, bot1

def find_opening(players, hands_players):
    # Find the holder of the highest double to start the game.
    six_six = {
        player: hand
        for player, hand in zip(players, hands_players)
            if (6, 6) in hand
    }
    starter = first_play(six_six)
    if starter is not None:
        return starter, (6, 6)

    # If the 6-6 is in the boneyard, use the highest double dealt to a player.
    for value in range(5, -1, -1):
        double = (value, value)
        for player, hand in zip(players, hands_players):
            if double in hand:
                return player, double

    # No double was dealt, so the first player opens with any tile.
    return players[0], None


def play_game():
    player_main, bot1 = username()
    players = [player_main, bot1]
    shuffled_pieces = shuffle_pieces(all_domino_pieces())
    hands_players = generate_hands(shuffled_pieces, len(players))
    buyable_pile = buyable_pieces(shuffled_pieces, hands_players)
    table = []

    print("LET'S PLAY DOMYTHON!")
    starter, opening_piece = find_opening(players, hands_players)
    if opening_piece is None:
        current_player = starter
        print(f"No double was dealt. {starter} starts.")
    else:
        starter_hand = hands_players[players.index(starter)]
        # Put the opening double on the table and remove it from that hand.
        play_piece(starter_hand, opening_piece, None, table)
        current_player = pass_turn(starter, players)
        print(f"{starter} opened with {opening_piece}.")

    consecutive_passes = 0

    while True:
        player_index = players.index(current_player)
        hand = hands_players[player_index]
        if current_player == bot1:
            played = opponent_play(hand, table)
        else:
            opponent_index = 1- player_index
            opponent_name = players[1]
            opponent_hand = hands_players[opponent_index]

            played = play_turn(
            current_player, hand, table, buyable_pile,
            opponent_name, opponent_hand)

        if played:
            consecutive_passes = 0
            if not hand:
                print(f"{current_player} has won the game!")
                return
        else:
            consecutive_passes += 1
            if consecutive_passes == len(players):
                print("Everyone passed. The game is blocked.")
                print("The winner is who has fewer points")
                sum_hands(hand)
                return

        current_player = pass_turn(current_player, players)


if __name__ == "__main__":
    play_game()
