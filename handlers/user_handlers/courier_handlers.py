import aiogram.exceptions
from aiogram import F
from loader import dp, db, bot
from keyboards.keyboards import *
from aiogram.filters import Command
import time
from datetime import datetime


@dp.callback_query(F.data.startswith("t|"))
async def take_order(call: types.CallbackQuery):
    couriers = await db.check_if_courier(call.message.chat.id)
    if not couriers:
        await call.answer("Ви не кур'єр")
    else:
        t, courier_id, order_id = call.data.split("|")
        order = await db.get_order_by_id(int(order_id))
        if order is None:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await call.message.answer('Замовлення видалено.')
        else:
            is_available = await db.if_courier_is_available(int(courier_id))
            if len(is_available) > 0:
                await call.message.answer(f'Виконайте минуле замовлення перед тим, як взяти наступне! ({[item["order_id"] for item in is_available]})')
            else:
                if order['courier'] is None:
                    await db.change_order_status(int(order_id), 2)
                    await db.set_courier_for_order(int(order_id), call.message.chat.id)

                    # USER
                    try:
                        # ADMINS
                        for admin in admins:
                            try:
                                await bot.send_message(admin, f"⚡️Замовлення #{order_id} взяте кур'єром id:<code>{call.message.chat.id}</code>.",
                                                       reply_markup=admin_order_notify(courier_id))
                            except aiogram.exceptions.TelegramBadRequest:
                                pass

                        # COURIER
                        try:
                            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                                reply_markup=courier_kb(user_id=order['user_id'],
                                                                                        courier_id=call.message.chat.id,
                                                                                        order_id=order_id,
                                                                                        delivering=True))
                            await call.message.answer(f'Ви взяли це замовлення! Доставте його у найкоротші строки та нажміть кнопку "Доставлено"')

                            await db.change_order_status(int(order_id), 2)
                            await bot.send_message(order['user_id'], f"⚡️Замовлення #{order_id} взяте кур'єром.\n", reply_markup=menu(order['user_id']))
                        except aiogram.exceptions.TelegramBadRequest:
                            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                                reply_markup=courier_kb(courier_id=call.message.chat.id,
                                                                                        order_id=order_id,
                                                                                        delivering=True))
                    except aiogram.exceptions.TelegramForbiddenError:
                        pass
                else:
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    await call.message.answer("Замовлення вже взяте іншим кур'єром", reply_markup=menu(call.message.chat.id))


@dp.callback_query(F.data.startswith("d|"))
async def delivered_order(call: types.CallbackQuery):
    couriers = await db.check_if_courier(call.message.chat.id)
    if not couriers:
        await call.answer("Ви не кур'єр")
    else:
        d, courier_id, order_id = call.data.split("|")
        order = await db.get_order_by_id(int(order_id))
        if order['status'] == 3:
            await call.answer("Замовлення вже доставлено")
        else:
            await db.change_order_status(int(order_id), 3)
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            converted_now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
            await db.set_order_time(int(order_id), converted_now)
            await db.add_earn_courier(order['price'], call.message.chat.id)
            await db.add_earn_stat(order['price'])
            await db.add_completed(call.message.chat.id)
            try:
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            except (Exception,):
                pass
            await call.message.answer('Замовлення доставлено!', reply_markup=menu(call.message.chat.id))
            try:
                await bot.send_message(order['user_id'], f'Замовлення #{order_id} доставлено! Дякуємо, що користуєтесь нашим сервісом!',
                                   reply_markup=menu(order['user_id']))
            except aiogram.exceptions.TelegramForbiddenError:
                pass
            for admin in admins:
                try:
                    await bot.send_message(admin, f"Кур'єр доставив замовлення #{order_id}",
                                           reply_markup=admin_order_notify(courier_id))
                except aiogram.exceptions.TelegramBadRequest:
                    pass


@dp.message(F.text, Command('tasks'))
async def get_tasks(message: types.Message):
    if await db.check_if_courier(message.chat.id):
        tasks = await db.get_free_tasks()
        print(len(tasks))
        print(tasks)
        if len(tasks) == 0:
            await message.answer('Замовлень немає.', reply_markup=menu(message.chat.id))
        else:
            await message.answer(f'Замовлення:', reply_markup=orders_list(tasks))


@dp.callback_query(F.data.startswith("o|"))
async def get_free_order(call: types.CallbackQuery):
    if await db.check_if_courier(call.message.chat.id):
        o, order_id = call.data.split("|")
        order = await db.get_order_by_id(int(order_id))
        text = f'⚡️ <b>Замовлення #{order_id}</b>(Код:<code>{str(order_id) + str(order["user_id"])[0:2]}</code>)\n\n'
        total_price = 0
        try:
            for item in order['bucket']:
                good = await db.get_good_by_good_id(item[1])
                text += f"⚡️<b>Товар:</b> {good['good_name']}\n"
                text += f"💸 <b>Ціна:</b> {good['price'] * item[2]}\n"
                text += f"📑 <b>Кількість:</b> {item[2]}\n\n"
                total_price += good['price'] * item[2]

            text += f"Загальна сума: <b>{total_price}ГРН</b>\n"
            text += f'Адреса: <b><code>{order["address"]}</code></b>\n'
            text += f'Контакт: <b>{order["contact"]}</b>\n'
            text += f'Коментар: <b>{order["comment"]}</b>\n'

            try:
                await call.message.answer(text, reply_markup=courier_kb(user_id=order['user_id'],
                                                                        courier_id=call.message.chat.id,
                                                                        order_id=order_id))
            except aiogram.exceptions.TelegramBadRequest:
                await call.message.answer(text, reply_markup=courier_kb(user_id=False,
                                                                        courier_id=call.message.chat.id,
                                                                        order_id=order_id))
        except TypeError:
            await call.answer('Замовлення неможливо доставить. Товара не існує.')
            try:
                await bot.send_message(order["user_id"], f'Замовлення #{order_id} неможливо доставити. Товара не існує.',
                                       reply_markup=menu(order['user_id']))
                await db.change_order_status(int(order_id), 3)
            except aiogram.exceptions.TelegramForbiddenError:
                pass
