import aiogram.exceptions
from aiogram import types
from config.cfg import admins
from aiogram.filters import BaseFilter
from keyboards.keyboards import courier_kb
from keyboards.admin_keyboards import admin_delete_order
from loader import db
import schedule
import asyncio
from threading import Thread

user_pagination = {}
admin_pagination = {}


class IsAdmin(BaseFilter):
    def __init__(self) -> None:  # Присваиваем self.admin_list список админов с конфига
        self.admins_list = admins

    async def __call__(self,
                       message: types.Message) -> bool:  # Возвращаем BOOL(True/False) если user.id не/cостоит в списке
        return message.from_user.id in self.admins_list


async def set_bucket_text(bucket) -> list:
    total_price = 0
    delivery_price = await db.get_price()
    text = ''
    for item in bucket['bucket']:
        try:
            good = await db.get_good_by_good_id(item[1])
            text += f"⚡️<b>Товар:</b> {good['good_name']}\n"
            text += f"💸 <b>Ціна:</b> {good['price'] * item[2]}\n"
            text += f"📑 <b>Кількість:</b> {item[2]}\n\n"
            total_price += good['price'] * item[2]
        except TypeError:
            pass

    text += f"Загальна сума: <b>{total_price}</b> + <b>{delivery_price}</b> ціна доставки."

    return [text, total_price, delivery_price]


async def send_couriers(order_id):
    couriers = await db.get_couriers()
    order = await db.get_order_by_id(int(order_id))
    text = f'⚡️ <b>Замовлення #{order_id}</b>(Код:<code>{str(order_id)+str(order["user_id"])[0:2]}</code>)\n\n'
    total_price = 0
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

    for courier in couriers:
        try:
            await bot.send_message(courier['id'], text,
                                   reply_markup=courier_kb(user_id=order['user_id'], courier_id=courier['id'], order_id=order_id))
        except aiogram.exceptions.TelegramBadRequest:
            await bot.send_message(courier['id'], text,
                                   reply_markup=courier_kb(user_id=False, courier_id=courier['id'], order_id=order_id))


async def send_admins(order_id):
    order = await db.get_order_by_id(int(order_id))
    # status = await mono.get_receipt(str(order_id)+str(order["user_id"])[0:2])
    # status = await mono.get_receipt("Test")
    text = f'⚡️ <b>Замовлення #{order_id}</b>(Код:<code>{str(order_id)+str(order["user_id"])[0:2]}</code>)\n\n'
    total_price = 0
    for item in order['bucket']:
        good = await db.get_good_by_good_id(item[1])
        text += f"⚡️<b>Товар:</b> {good['good_name']}\n"
        text += f"💸 <b>Ціна:</b> {good['price'] * item[2]}\n"
        text += f"📑 <b>Кількість:</b> {item[2]}\n\n"
        total_price += good['price'] * item[2]

    text += f"Загальна сума: <b>{total_price}ГРН (Без доставки)</b>\n"
    text += f'Адреса: <b>{order["address"]}</b>\n'
    text += f'Контакт: <b>{order["contact"]}</b>\n'
    text += f'Коментар: <b>{order["comment"]}</b>\n\n'
    text += f'ID Юзера: <code>{order["user_id"]}</code>'

    # if status is not False:
    #     text += "Інформація по оплаті:\n"
    #     text += f"Сумма за доставку: {status['sum']}\n"
    #     text += f"Актуальний баланс: {status['balance']}\n"
    #     text += f"{status['description']}\n"
    #     text += f"ID оплати: {status['id']}\n"
    #     text += f"Дата: {status['time']}"

    for admin in admins:
        try:
            await bot.send_message(admin, text, reply_markup=admin_delete_order(order_id))
        except aiogram.exceptions.TelegramBadRequest:
            pass


# async def run_pending():
#     while True:
#         schedule.run_pending()
#         await asyncio.sleep(1)


# x = schedule.every().day.at('01:00').do(clear_earned())
# z = schedule.every().day.at('01:00').do(clear_delivered())
#
# clear_thread = Thread(target=asyncio.run, args=(run_pending(),))
# clear_thread.start()