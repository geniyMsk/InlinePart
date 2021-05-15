import emoji, sqlite3, json
from emoji import emojize
from loader import bot, dp
from aiogram import types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

class states(StatesGroup):
    on = State()
    off=State()

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="1", callback_data='1'),
            InlineKeyboardButton(text="2", callback_data='2'),
            InlineKeyboardButton(text="3", callback_data='3')
        ],
        [
            InlineKeyboardButton(text="4", callback_data='4'),
            InlineKeyboardButton(text="5", callback_data='5')
        ]

])
pressed = []


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(text='Какой-то текст', reply_markup=inline_keyboard)
    await states.on.set()


@dp.callback_query_handler(state=states.on)
async def inline(query: CallbackQuery):
    i = 1
    message_id = query.message.message_id
    chatid = query.from_user.id
    keyboard=query.message.reply_markup
    while i<=5:
        if query.data==f'{i}':
            if i<=3:
                text_button = keyboard.inline_keyboard[0][i-1]['text']

                if text_button == f'{i}':
                    keyboard.inline_keyboard[0][i - 1]['text'] = emojize(f'{i}:check_mark_button:')
                    pressed.append(i)
                    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=message_id, reply_markup=keyboard)
                else:
                    pressed.remove(i)
                    keyboard.inline_keyboard[0][i - 1]['text'] = emojize(f'{i}')
                    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=message_id,reply_markup=keyboard)

            else:
                text_button = keyboard.inline_keyboard[1][i - 4]['text']
                if text_button == f'{i}':
                    keyboard.inline_keyboard[1][i - 4]['text'] = emojize(f'{i}:check_mark_button:')
                    pressed.append(i)
                    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=message_id,
                                                        reply_markup=keyboard)
                else:
                    keyboard.inline_keyboard[1][i - 4]['text'] = emojize(f'{i}')
                    pressed.remove(i)
                    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=message_id,reply_markup=keyboard)
        i+=1
    with sqlite3.connect('server.db') as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE, buttons TEXT)""")
        try:
            cursor.execute(f"""INSERT INTO users (id, buttons) VALUES ({chatid}, '{pressed}')""")
        except:
            cursor.execute(f"""UPDATE users SET buttons = '{pressed}' WHERE id={chatid}""")

@dp.message_handler(commands=['button'], state='*')
async def button(message: types.Message):
    chatid = message.from_user.id
    with sqlite3.connect('server.db') as db:
        cursor = db.cursor()
        buttons = json.loads(cursor.execute(f"""SELECT buttons FROM users WHERE id={chatid}""").fetchone()[0])
        text=''
        for button in buttons:
            text += f'{button}, '


        x=len(text)-2
        await message.answer(text='У вас нажаты кнопки: '+text[:x])
@dp.message_handler(commands=['stop'], state='*')
async def stop(message: types.Message):
    await message.answer("Нельзя изменять символ на кнопках")
    await states.off.set()