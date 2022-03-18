from random import choice


def game(select):
    # player will input int 1-3

    option= {
        'ROCK': 'SCISSORS',
        'SCISSORS': 'PAPER',
        'PAPER': 'ROCK'
    }

    bot = choice(list(option)) # computers choice
    plyr = select.upper()   # players choice

    #return SCORE, computer's choice, player's choice
    if bot == plyr:
        return 0, bot, plyr
    elif bot == option[plyr]:
        return 1, bot, plyr
    else:
        return -1, bot, plyr

# A = {
#     1: 'SCISSORS',
#     2: 'PAPER',
#     3: 'ROCK'
# }

# print(game(A[1]))
# print(game(A[2]))
# print(game(A[3]))