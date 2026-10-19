from shuffling import generate_hands

player = []

print("Bem-vindo ao Domython!")

def how_many_players():
    while True:
        try:
            players_num = int(input("Número de jogadores (2-4): "))
            if players_num < 2 or players_num > 4:
                print("Número de jogadores inválido. Por favor, insira um número entre 2 e 4.")
                continue
        except ValueError:
            print("Entrada inválida. Por favor, insira um número de jogadores válidos.")
        else:
            return players_num


def get_players(): 
    players_num = how_many_players()
    for i in range(players_num):
        while True:
            nickname = input("Enter your nickname: ")
            if nickname in player:
                print("This nickname is already exists. Choose another one.")
                continue
            break
        player.append(nickname)
    return player
