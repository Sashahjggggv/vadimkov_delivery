from aiogram import F
from loader import dp, db, bot
from keyboards.keyboards import *
from states.states import ChoseAmount
from aiogram.fsm.context import FSMContext
from utils.some_shit import user_pagination


@dp.message(F.text == '👤 Профіль')
async def profile(message: types.Message):
    orders = await db.get_payed_order_by_user_id(message.chat.id)
    await message.answer(f'<b>🔒 Ваш айді:</b> <code>{message.chat.id}</code>\n\nВаші замовлення 👇🏻',
                         reply_markup=profile_orders_list(orders))


@dp.callback_query(F.data.startswith("po"))
async def profile_order(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    order_id = int(call.data.split('|')[-1])
    order = await db.get_order_by_id(order_id)
    text = f'<b>Замовлення #<code>{order["order_id"]}</code></b>\n' \
           f'<b>Ціна</b>: {order["price"]}\n\n'
    print(order)
    for item in order['bucket']:
        try:
            good = await db.get_good_by_good_id(item[1])
            text += f"⚡️<b>Товар:</b> {good['good_name']}\n"
            text += f"💸 <b>Ціна:</b> {good['price'] * item[2]}\n"
            text += f"📑 <b>Кількість:</b> {item[2]}\n\n"
        except TypeError:
            text = 'Товар який ви замовляли більше не доступний в магазині.\n'

    text += f"<b>📦 Кур'єр:</b> <code>{order['courier']}</code>"

    await call.message.answer(text, reply_markup=profile_back_list())


@dp.callback_query(F.data == 'back_to_profile_list')
async def back_to_p_list(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await profile(call.message)

