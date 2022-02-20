import random


stock = []
player = []
computer = []
domino_snake = []
status = ''

# filling out the stock with 28 valid(unique) dominoes
for i in range(7):
    for j in range(7):
        if [j, i] in stock:
            continue
        stock.append([i, j])


# dealing random dominoes to the player and the computer
def deal_dominoes():
    global player
    global computer
    global stock
    global status
    global domino_snake

    random_dominoes = random.sample(stock, 14)
    computer = random_dominoes[:7]
    player = random_dominoes[7:]
    stock_temp = [x for x in stock if x not in random_dominoes]
    stock = stock_temp
    double_dominoes = [x for x, y in player + computer if x == y]

    # if no one has been dealt a double domino we deal again
    if len(double_dominoes) == 0:
        deal_dominoes()

    # player with the highest double domino starts the game by playing it
    else:
        m = max(double_dominoes)
        domino_snake = [[m, m]]
        if [m, m] in player:
            player.remove([m, m])
            status = 'computer'
        else:
            computer.remove([m, m])
            status = 'player'


# game is over if a player is left with 0 dominoes or if neither player can play a move legally
def game_over(pl, comp, snake):
    flat_list = []
    for x in snake:
        for y in x:
            flat_list.append(y)
    if len(pl) == 0:
        return 1
    elif len(comp) == 0:
        return 2
    elif snake[0][0] == snake[-1][1] and flat_list.count(snake[0][0]) == 8:
        return -1
    else:
        return 0


# called by either player or computer and makes a move after it is confirmed to be legal
def make_move(on_move, move):

    if move == 0 and len(stock) != 0:
        piece = random.choice(stock)
        on_move.append(piece)
        stock.remove(piece)
    elif move < 0:
        move = abs(move)
        if on_move[move - 1][0] == domino_snake[0][0]:
            on_move[move - 1][0], on_move[move - 1][1] = on_move[move - 1][1], on_move[move - 1][0]
        domino_snake.insert(0, on_move[move - 1])
        on_move.remove(on_move[move - 1])
    elif move > 0:
        if on_move[move - 1][1] == domino_snake[-1][1]:
            on_move[move - 1][0], on_move[move - 1][1] = on_move[move - 1][1], on_move[move - 1][0]
        domino_snake.append(on_move[move - 1])
        on_move.remove(on_move[move - 1])


# a move is legal if a domino being played contains a value on the chosen end of the snake
def is_move_legal(on_move, move):
    if move < 0:
        move = abs(move)
        if domino_snake[0][0] in on_move[move - 1]:
            return True
        else:
            return False
    elif move > 0:
        if domino_snake[-1][1] in on_move[move - 1]:
            return True
        else:
            return False
    return True


# called when it is the players turn
def player_makes_move():
    global status

    while True:
        try:
            move = int(input())
            if abs(move) > len(player):
                print("Invalid input. ", end='')
                raise Exception
            if not is_move_legal(player, move):
                print("Illegal move. ", end='')
                raise Exception
        except (ValueError, Exception):
            print("Please try again.")
        else:
            break

    make_move(player, move)
    status = 'computer'


# called when it is the computers move
def computer_makes_move():
    global status

    input()
    ranked_moves_dict = rank_computers_moves()

    # makes a move by ranking the dominoes the computer has and getting rid of the least rare domino
    while True:
        if len(computer) == 0 or len(ranked_moves_dict) == 0:
            make_move(computer, 0)
            break

        move = max(ranked_moves_dict) * -1
        if is_move_legal(computer, move):
            make_move(computer, move)
            break
        else:
            move *= -1
            if is_move_legal(computer, move):
                make_move(computer, move)
                break
            else:
                del ranked_moves_dict[move]

    status = 'player'


# rank computers moves by rarity and returns a dictionary with moves as keys and rarity scores as values
def rank_computers_moves():
    value_count = {x: 0 for x in range(7)}
    comp_and_snake = computer + domino_snake
    for x in comp_and_snake:
        for y in x:
            value_count[y] += 1

    ranked_moves = {}
    for x in range(1, len(computer) + 1):
        ranked_moves[x] = value_count[computer[x - 1][0]] + value_count[computer[x - 1][1]]

    return ranked_moves


# starts the game after the dominoes have been dealt
def play_game(pl, comp, snake):
    global status

    while game_over(pl, comp, snake) == 0:
        output(status)
        if status == 'player':
            player_makes_move()
        else:
            computer_makes_move()

    result = game_over(pl, comp, snake)
    if result == 1:
        status = 'player won'
    elif result == 2:
        status = 'computer won'
    else:
        status = "draw"
    output(status)


# prints the entire snake if its length is < 6. Otherwise, it prints the first and last 3 dominoes
def print_snake():
    if len(domino_snake) > 6:
        for x in range(2):
            print(str(domino_snake[x]) + ',', end='')
        print(str(domino_snake[2]), end='')
        print('...', end='')
        for x in range(-3, -1):
            print(str(domino_snake[x]) + ',', end='')
        print(str(domino_snake[-1]))
    else:
        for x in range(len(domino_snake) - 1):
            print(str(domino_snake[x]) + ',', end='')
        print(str(domino_snake[-1]))


# this is printed out every turn
def output(st):
    print('=' * 70)
    print('Stock size:', len(stock))
    print('Computer pieces:', len(computer), '\n')
    print_snake()
    print('\nYour pieces:')
    for x in range(len(player)):
        print(str(x + 1) + ':' + str(player[x]))
    print()
    if st == 'computer':
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif st == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
    elif st == 'player won':
        print('Status: The game is over. You won!')
    elif st == 'computer won':
        print('Status: The game is over. The computer won!')
    else:
        print("Status: The game is over. It's a draw!")


def main():
    deal_dominoes()
    play_game(player, computer, domino_snake)


if __name__ == '__main__':
    main()
