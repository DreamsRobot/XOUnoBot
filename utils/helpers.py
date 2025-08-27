import random

# XO Helpers
def check_winner(board):
    win_pos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for pos in win_pos:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != '':
            return board[pos[0]]
    if '' not in board:
        return "Draw"
    return None

def board_to_text(board):
    return "\n".join([
        f"{board[0] or '1'} | {board[1] or '2'} | {board[2] or '3'}",
        f"{board[3] or '4'} | {board[4] or '5'} | {board[5] or '6'}",
        f"{board[6] or '7'} | {board[7] or '8'} | {board[8] or '9'}"
    ])

# Uno Helpers
def get_uno_deck():
    colors = ["red", "yellow", "green", "blue"]
    numbers = [str(i) for i in range(0,10)]
    deck = []
    for c in colors:
        for n in numbers:
            deck.append(f"{c}_{n}")
        deck.append(f"{c}_skip")
        deck.append(f"{c}_reverse")
        deck.append(f"{c}_draw2")
    deck += ["wild", "wild_draw4"]*4
    random.shuffle(deck)
    return deck

def is_playable(card, top_card):
    if card.startswith("wild"):
        return True
    return card.split("_")[0] == top_card.split("_")[0] or card.split("_")[1] == top_card.split("_")[1]

def draw_cards(deck, n=1):
    drawn = []
    for _ in range(n):
        if not deck:
            break
        drawn.append(deck.pop())
    return drawn
