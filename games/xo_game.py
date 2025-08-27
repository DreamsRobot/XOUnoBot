# XOUnoBot/games/xo_game.py

import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from XOUnoBot import app   # import your bot's client instance

# In-memory XO game storage
active_games = {}  # {chat_id: {"board": list, "turn": user_id, "players": [user1, user2]}}


def render_board(board):
    """Render XO board into buttons"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(board[0], callback_data="xo_0"),
                InlineKeyboardButton(board[1], callback_data="xo_1"),
                InlineKeyboardButton(board[2], callback_data="xo_2"),
            ],
            [
                InlineKeyboardButton(board[3], callback_data="xo_3"),
                InlineKeyboardButton(board[4], callback_data="xo_4"),
                InlineKeyboardButton(board[5], callback_data="xo_5"),
            ],
            [
                InlineKeyboardButton(board[6], callback_data="xo_6"),
                InlineKeyboardButton(board[7], callback_data="xo_7"),
                InlineKeyboardButton(board[8], callback_data="xo_8"),
            ],
        ]
    )


def check_winner(board):
    """Check winner of XO game"""
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "⬜":
            return board[a]
    if "⬜" not in board:
        return "draw"
    return None


@app.on_message(filters.command("start_xo"))
async def start_xo(_, m: Message):
    chat_id = m.chat.id
    if chat_id in active_games:
        return await m.reply("⚠️ A game is already active in this chat!")

    if not m.reply_to_message:
        return await m.reply("Reply to a user to challenge them to XO!")

    player1 = m.from_user.id
    player2 = m.reply_to_message.from_user.id

    # Initialize game
    board = ["⬜"] * 9
    active_games[chat_id] = {"board": board, "turn": player1, "players": [player1, player2]}

    await m.reply(
        f"🎮 XO Game Started!\n\n{m.from_user.mention} (❌) vs {m.reply_to_message.from_user.mention} (⭕)\n\n"
        f"Turn: {m.from_user.mention}",
        reply_markup=render_board(board)
    )


@app.on_callback_query(filters.regex(r"^xo_\d$"))
async def xo_move(_, cq):
    chat_id = cq.message.chat.id
    if chat_id not in active_games:
        return await cq.answer("⚠️ No active game!", show_alert=True)

    game = active_games[chat_id]
    board = game["board"]
    player1, player2 = game["players"]

    pos = int(cq.data.split("_")[1])
    user_id = cq.from_user.id

    if user_id != game["turn"]:
        return await cq.answer("⚠️ It's not your turn!", show_alert=True)

    if board[pos] != "⬜":
        return await cq.answer("⚠️ That spot is already taken!", show_alert=True)

    # Assign symbol
    symbol = "❌" if user_id == player1 else "⭕"
    board[pos] = symbol

    # Switch turn
    game["turn"] = player2 if user_id == player1 else player1

    winner = check_winner(board)

    if winner == "❌":
        del active_games[chat_id]
        return await cq.message.edit_text(
            f"🏆 {cq.from_user.mention} (❌) wins!",
            reply_markup=render_board(board)
        )
    elif winner == "⭕":
        del active_games[chat_id]
        return await cq.message.edit_text(
            f"🏆 {cq.from_user.mention} (⭕) wins!",
            reply_markup=render_board(board)
        )
    elif winner == "draw":
        del active_games[chat_id]
        return await cq.message.edit_text(
            "🤝 It's a draw!",
            reply_markup=render_board(board)
        )

    # Update board
    next_player = game["turn"]
    await cq.message.edit_text(
        f"🎮 XO Game\nTurn: <a href='tg://user?id={next_player}'>Next Player</a>",
        reply_markup=render_board(board)
    )


@app.on_message(filters.command("cancel_xo"))
async def cancel_xo(_, m: Message):
    chat_id = m.chat.id
    if chat_id not in active_games:
        return await m.reply("⚠️ No active game to cancel.")

    del active_games[chat_id]
    await m.reply("🛑 XO Game has been cancelled.")
