from aiogram import F
from loader import dp, db
from utils.some_shit import IsAdmin
from keyboards.admin_keyboards import *
import time


@dp.message(F.text == 'Статистика', IsAdmin())
async def stat(message: types.Message):
    data = await db.get_stat()
    orders = await db.get_delivered_orders()
    users = await db.get_all_users()
    await message.answer(f'Зароблено (Оборот): <b>{data["earned"]} UAH</b>\n'
                         f'Людей в боті: <b>{len(users)}</b>\n', reply_markup=admin_kb())
