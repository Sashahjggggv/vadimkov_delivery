from loader import dp, db, bot
from config.cfg import admins
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards.keyboards import *
from aiogram import F


@dp.message(Command('start'))
async def start(message: types.Message):
    await db.check_user(message.chat.id)
    await message.answer('Вітаємо у магазині!', reply_markup=menu(message.chat.id))


@dp.message(F.text == '🛒 Каталог')
async def open_categories(message: types.Message):
    categories = await db.get_all_categories()
    await message.answer('Каталог: ', reply_markup=catalog_categories(categories))