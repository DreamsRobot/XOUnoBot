from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from games import xo_game, uno_game

app = Client("xo_uno_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# XO handlers
app.add_handler(xo_game.start_xo_handler)
app.add_handler(xo_game.play_xo_handler)
app.add_handler(xo_game.score_xo_handler)
app.add_handler(xo_game.cancel_xo_handler)

# Uno inline
app.add_handler(uno_game.inline_handler)

print("✅ XO & Uno Bot is running...")
app.run()
