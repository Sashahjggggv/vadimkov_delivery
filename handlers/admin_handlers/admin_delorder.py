import types

import aiogram.exceptions

from loader import dp, db, bot, rt
from aiogram.filters import Command, CommandObject, BaseFilter
from keyboards.admin_keyboards import *
from keyboards.keyboards import menu
from aiogram import F
from aiogram.fsm.context import FSMContext
from config.cfg import admins
from utils.some_shit import admin_pagination
from states.admin_states import *


@dp.callback_query(F.data.startswith("delo|"))
async def del_order(call: types.CallbackQuery, state: FSMContext):
    order_id = int(call.data.split("|")[-1])
    order = await db.get_order_by_id(int(order_id))
    if order is None:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer('Замовлення вже видалено.')
    else:
        if order['status'] == 2:
            await call.message.answer('Візміть до уваги, що замовлення вже доставляється.')

        await call.message.answer('Ви хочете заплатить роялті своєму кодеру?', reply_markup=admin_delete_o_confirm(order_id))
        await state.set_state(DeleteOrder.q1)


@dp.callback_query(F.data.startswith("cdelo|"), DeleteOrder.q1)
async def del_order(call: types.CallbackQuery, state: FSMContext):
    order_id = int(call.data.split("|")[-1])
    order = await db.get_order_by_id(int(order_id))
    # await db.recover_orders(order[1], order[2])
    await db.delete_order(int(order_id))
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'Замовлення #{order_id} видалено!')
    try:
        await bot.send_message(order['user_id'], f"Замовлення #{order_id} відхилено!", reply_markup=menu(order['user_id']))
    except aiogram.exceptions.TelegramForbiddenError:
        pass
    await state.clear()


@dp.callback_query(F.data == 'cancel_delete')
async def del_order(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer('Відміна!')