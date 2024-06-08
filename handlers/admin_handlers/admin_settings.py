import types

from aiogram import F
from loader import dp, db, bot
from states.admin_states import *
from keyboards.admin_keyboards import *
from aiogram.fsm.context import FSMContext
from utils.some_shit import IsAdmin


@dp.message(F.text == 'Налаштування бота', IsAdmin())
async def settings_menu(message: types.Message):
    settings = await db.get_settings()
    await message.answer('<b>Налаштування:</b>\n\n'
                         f'Робочий час: <b>{settings["work_time"][0]}-{settings["work_time"][1]}\n</b>'
                         f'Ціна доставки: <b>{settings["price"]} UAH</b>',
                         reply_markup=settings_kb())


@dp.callback_query(F.data == 'change_time')
async def settings_change_time(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть новий робочий час у форматі <b><i>10-22</i></b>', reply_markup=cancel_settings())
    await state.set_state(Settings.Time.q1)


@dp.message(F.text.contains('-'), Settings.Time.q1)
async def settings_change_time(message: types.Message, state: FSMContext):
    start, end = message.text.split('-')
    if start.isdigit() and end.isdigit():
        start, end = int(start), int(end)
        if 0 <= start <= 24 and 0 <= end <= 24:
            await db.set_time(start, end)
            await message.answer('Новий час встановлено.', reply_markup=admin_kb())
            await state.clear()
        else:
            await message.answer('Введіть час у правильному форматі.', reply_markup=cancel_settings())
            return
    else:
        await message.answer('Введіть час у правильному форматі.', reply_markup=cancel_settings())
        return


@dp.message(F.text, Settings.Time.q1)
async def settings_change_time(message: types.Message, state: FSMContext):
    await message.answer('Введіть час у правильному форматі.', reply_markup=cancel_settings())
    return


@dp.callback_query(F.data == 'change_d_price')
async def settings_change_price(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть нову ціну за доставку цифрами (Без копійок).', reply_markup=cancel_settings())
    await state.set_state(Settings.Price.q1)


@dp.message(F.text, Settings.Price.q1)
async def settings_change_price(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        price = float(message.text)
        await db.change_price(price)
        await message.answer('Ціна змінена.', reply_markup=admin_kb())
        await state.clear()
    else:
        await message.answer('Введіть ціну цифрами.', reply_markup=cancel_settings())
        return


@dp.callback_query(F.data == 'back_to_settings')
async def back_to_settings(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if await state.get_state():
        await state.clear()
    await settings_menu(call.message)
