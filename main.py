import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8035290236:AAGkyvJQllGr0gcYO0CizNwHOM_t3K79R6Q"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

game_board = [' '] * 9
player_turn = 'X'

def check_winner():
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_combinations:
        if game_board[a] == game_board[b] == game_board[c] and game_board[a] != ' ':
            return game_board[a]
    if ' ' not in game_board:
        return 'Draw'
    return None

def render_board():
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=game_board[i] if game_board[i] != ' ' else str(i + 1),
                                    callback_data=str(i)) for i in range(9)]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    global game_board, player_turn
    game_board = [' '] * 9
    player_turn = 'X'
    await message.answer("Игра в Крестики-нолики! Игрок X ходит первым.", reply_markup=render_board())

@dp.callback_query_handler()
async def handle_move(call: types.CallbackQuery):
    global player_turn
    index = int(call.data)
    if game_board[index] == ' ':
        game_board[index] = player_turn
        winner = check_winner()
        if winner:
            await call.message.edit_text(f'Победитель 🎉: {winner}' if winner != 'Draw' else 'Ничья!',
                                         reply_markup=None)
        else:
            player_turn = 'O' if player_turn == 'X' else 'X'
            await call.message.edit_text(f'Ход игрока {player_turn}:', reply_markup=render_board())
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
