from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command

TOKEN = '5311392408:AAHg8Q5VdFfgdnqhrmgNOPthjRIXUo_l3-U'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command(commands=['start']))
async def start(msg: types.Message):
    await msg.answer(f'Лол, {msg.from_user.full_name}, ты кринж')
