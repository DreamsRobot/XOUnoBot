from pyrogram import filters
from pyrogram.types import InlineQueryResultCachedSticker, InlineQuery, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from utils.helpers import get_uno_deck
from utils.database import get_collection
import json
import random

uno_collection = get_collection("uno_games")

with open("stickers/uno_stickers.json") as f:
    STICKERS = json.load(f)

# Inline query to show cards
async def inline_handler(client, inline_query: InlineQuery):
    results = []
    deck = get_uno_deck()
    for i in range(5):
        card = deck[i]
        sticker_id = STICKERS.get(card, STICKERS["red_0"])
        results.append(
            InlineQueryResultCachedSticker(
                id=str(i),
                sticker_file_id=sticker_id
            )
        )
    await inline_query.answer(results, cache_time=0)

inline_handler = filters.inline_query()
