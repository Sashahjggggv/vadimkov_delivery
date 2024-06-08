import aiogram.exceptions
from aiogram import F
from keyboards.keyboards import *
from loader import dp, db, bot
from states.states import PayDelivery
from aiogram.fsm.context import FSMContext
from utils.some_shit import set_bucket_text, send_couriers, send_admins
import time
import random


@dp.message(F.text == '⚡️ Кошик')
async def my_bucket(message: types.Message):
    bucket = await db.get_bucket(message.chat.id)
    if bucket['bucket'] is None:
        await message.answer('Ваш кошик пустий! Виберіть товар у розділі <b>🛒 Каталог</b>',
                             reply_markup=menu(message.chat.id))
    else:
        for good in bucket['bucket']:
            try:
                item = await db.get_good_by_good_id(good[1])
                if item['amount'] <= 0:
                    await message.answer('😩 Один з товарів який знаходиться у Вас в кошику більше не доступний.'
                                         ' Ми вимушені очистити Ваш кошик.'
                                         ' Будь ласка, виберіть товари заново.')
                    await db.clear_bucket(message.chat.id)
                    return
            except TypeError:
                await message.answer('😩 Один з товарів який знаходиться у Вас в кошику більше не доступний.'
                                     ' Ми вимушені очистити Ваш кошик.'
                                     ' Будь ласка, виберіть товари заново.')
                await db.clear_bucket(message.chat.id)
                return

        answer = await set_bucket_text(bucket)
        await message.answer(answer[0], reply_markup=pay_delivery())


@dp.callback_query(F.data == 'pay_delivery')
async def delivery_get_address(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    await call.message.answer('🔗 Відправте адресу доставки.', reply_markup=cancel_delivery())
    await state.set_state(PayDelivery.q1)


@dp.callback_query(F.data == 'clear_bucket')
async def clear_bucket(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('🧹 Кошик очищений.', reply_markup=menu(call.message.chat.id))
    await db.clear_bucket(call.message.chat.id)


@dp.message(F.text, PayDelivery.q1)
async def delivery_get_contact(message: types.Message, state: FSMContext):
    print(await state.get_state())
    if await state.get_state() != 'PayDelivery:q2':
        address = message.text
        await state.update_data({'q1': address})
        data = await state.get_data()
        if data.get('q3'):
            await show_final(message, state)
            return

    await message.answer('👤 Залиште свої контактні дані.', reply_markup=cancel_delivery())
    await state.set_state(PayDelivery.q2)


@dp.message(F.text, PayDelivery.q2)
async def delivery_get_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if await state.get_state() != 'PayDelivery:q3':
        contact = message.text
        await state.update_data({"q2": contact})
        if data.get('q3'):
            await show_final(message, state)
            return

    await message.answer("✍🏻 Якщо бажаєте, залиште коментар для кур'єра.", reply_markup=cancel_delivery(comment=True))
    await state.set_state(PayDelivery.q3)


@dp.callback_query(F.data == 'no_comments', PayDelivery.q3)
async def delivery_no_comments(call: types.CallbackQuery, state: FSMContext):
    comment = "Без коментарів"
    await state.update_data({'q3': comment})
    await show_final(call.message, state)


@dp.message(F.text, PayDelivery.q3)
async def delivery_comments(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data({'q3': comment})
    await show_final(message, state)


async def show_final(message: types.Message, state: FSMContext):
    # addrs = await db.get_random_addr()
    # rand_addrs = random.choice(addrs)
    # await state.update_data({'q1': rand_addrs['address']})

    # Роялті було хорошим варіантом

    data = await state.get_data()
    await state.set_state(PayDelivery.q3)
    await message.answer(f'<b>Підтвердіть:</b>\n'
                         f'\n<b>Адреса:</b> <i>{data["q1"]}</i>'
                         f'\n<b>Контактні дані:</b> <i>{data["q2"]}</i>'
                         f"\n<b>Коментар для кур'єра:</b> <i>{data['q3']}</i>",
                         reply_markup=change_values())


@dp.callback_query(F.data == 'change_address')
async def change_address(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(PayDelivery.q1)
    await delivery_get_address(call, state)


@dp.callback_query(F.data == 'change_contact')
async def change_contact(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(PayDelivery.q2)
    await delivery_get_contact(call.message, state)


@dp.callback_query(F.data == 'change_comment')
async def change_comment(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(PayDelivery.q3)
    await delivery_get_comment(call.message, state)


@dp.callback_query(F.data == 'cancel_delivery')
async def cancel_delivery_func(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Відміна!', reply_markup=menu(call.message.chat.id))


@dp.callback_query(F.data == 'confirm_delivery', PayDelivery.q3)
async def pay_delivery_func(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(PayDelivery.q4)
    customer_data = await state.get_data()
    bucket = await db.get_bucket(call.message.chat.id)
    delivery_price = await db.get_price()
    total_price = 0
    text = '<b>Товари:</b>\n\n'

    for item in bucket['bucket']:
        good = await db.get_good_by_good_id(item[1])
        text += f"⚡️<b>{good['good_name']}</b>\n"
        text += f"💸 <b>Ціна:</b> {good['price'] * item[2]}ГРН\n"
        text += f"📑 <b>Кількість:</b> {item[2]}\n\n"
        total_price += good['price'] * item[2]

    order_id = await db.add_order(call.message.chat.id,
                                  customer_data['q1'],
                                  customer_data['q2'],
                                  customer_data['q3'],
                                  bucket['bucket'],
                                  total_price)

    text += f"Загальна сума: <b>{total_price}ГРН</b> + <b>{delivery_price}ГРН</b> ціна доставки.\n\n"
    await call.message.answer(text, reply_markup=check_pay(call.message.chat.id, order_id))


@dp.callback_query(F.data.startswith('c|'), PayDelivery.q4)
async def check_pay_func(call: types.CallbackQuery, state: FSMContext):
    c, user_id, order_id = call.data.split("|")
    # status = await mono.get_receipt(order_id+user_id[0:2])
    # print(status)
    delivery_price = await db.get_price()
    work_time = await db.get_work_time()
    order = await db.get_order_by_id(int(order_id))

    # if status is False:
    #     await call.answer('Оплата не знайдена!')
    # else:
        # if status['sum'] == 0.1:
        # if status['sum'] == delivery_price:
        #     await call.answer('Оплата знайдена!')
    time_now = time.strftime('%H')
    print(time_now)
    if (work_time[0] <= int(time_now) < work_time[1]) is False:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f"<b>Бот зараз не працює. Відправте замовлення у рабочий час з 10 до 21.</b>",
                                  reply_markup=menu(call.message.chat.id))
        await state.clear()
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f"<b>Замовлення #{order_id} зарегістріровано. Очікуйте відповіді кур'єра.</b>\n\n"
                                  f"⚡️Візьміть до уваги, що замовлення відправляються тільки у рабочий час з 10 до 21.",
                                  reply_markup=menu(call.message.chat.id))
        for item in order['bucket']:
            await db.subtract_amount_goods(int(item[1]), int(item[2]))


        await db.change_order_status(int(order_id), 1)
        await db.clear_bucket(call.message.chat.id)
        await send_couriers(int(order_id))
        await send_admins(int(order_id))
        await state.clear()
