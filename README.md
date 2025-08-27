# XOUnoBot

#🃏 XO & UNO Telegram Bot
This is a Telegram bot that allows users to play XO (Tic-Tac-Toe) in groups and UNO in inline mode using stickers.
The bot stores game states and scores in MongoDB and supports inline buttons for Uno actions.
Features
XO Game (Group Chat)
/startgame – Start a new XO game
/play <position> – Play your turn (positions 1–9)
/score – Check current game scores
/cancel – Cancel the ongoing XO game
Shows a visual board in messages
Alternates turns automatically between X and O
UNO Game (Inline Mode)
Type @BotUsername in any chat to start inline Uno
Shows cards as stickers
Inline buttons for:
Draw card
Play card
Skip, Reverse, Wild actions
Game logic with playable card rules
Stores game state in MongoDB for each user
