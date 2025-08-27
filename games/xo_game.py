from pyrogram import filters
from pyrogram.types import Message
from utils.database import get_collection
from utils.helpers import check_winner, board_to_text

xo_collection = get_collection("xo_games")

async def start_xo(client, message: Message):
    chat_id = message.chat.id
    if xo_collection.find_one({"chat_id": chat_id}):
        await message.reply("❌ Game already started!")
        return
    xo_collection.insert_one({
        "chat_id": chat_id,
        "board": ['']*9,
        "turn": "X"
    })
    await message.reply("✅ XO Game started!\nX goes first.\nUse /play <position> to play.\n\n" +
                        board_to_text(['']*9))

async def play_xo(client, message: Message):
    chat_id = message.chat.id
    try:
        user_move = int(message.text.split()[1]) - 1
    except:
        await message.reply("❌ Usage: /play <position 1-9>")
        return
    game = xo_collection.find_one({"chat_id": chat_id})
    if not game:
        await message.reply("❌ Start a game first with /startgame")
        return
    board = game["board"]
    turn = game["turn"]
    if board[user_move] != '':
        await message.reply("❌ Position already taken!")
        return
    board[user_move] = turn
    winner = check_winner(board)
    if winner:
        await message.reply(f"🏆 Winner: {winner}" if winner != "Draw" else "🤝 It's a Draw!")
        xo_collection.delete_one({"chat_id": chat_id})
    else:
        xo_collection.update_one({"chat_id": chat_id}, {"$set": {"board": board, "turn": "O" if turn=="X" else "X"}})
        await message.reply(f"Next turn: {'O' if turn=='X' else 'X'}\n\n" +
                            board_to_text(board))

async def score_xo(client, message: Message):
    await message.reply("📊 XO score tracking not implemented yet.")

async def cancel_xo(client, message: Message):
    chat_id = message.chat.id
    xo_collection.delete_one({"chat_id": chat_id})
    await message.reply("❌ XO Game canceled.")

start_xo_handler = filters.command("startgame") & filters.group
start_xo_handler = start_xo_handler.create(lambda c, m: start_xo(c, m))

play_xo_handler = filters.command("play") & filters.group
play_xo_handler = play_xo_handler.create(lambda c, m: play_xo(c, m))

score_xo_handler = filters.command("score") & filters.group
score_xo_handler = score_xo_handler.create(lambda c, m: score_xo(c, m))

cancel_xo_handler = filters.command("cancel") & filters.group
cancel_xo_handler = cancel_xo_handler.create(lambda c, m: cancel_xo(c, m))
