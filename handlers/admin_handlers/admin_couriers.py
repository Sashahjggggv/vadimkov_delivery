import types
from loader import dp, db, bot, rt
from aiogram.filters import Command, CommandObject, BaseFilter
from keyboards.admin_keyboards import *
from aiogram import F
from aiogram.fsm.context import FSMContext
from config.cfg import admins
from utils.some_shit import admin_pagination
from states.admin_states import *
from utils.some_shit import IsAdmin


@dp.message(F.text == "Кур'єри", IsAdmin())
async def couriers_menu(message: types.Message):
    couriers = await db.get_couriers()
    await message.answer("Кур'єри", reply_markup=couriers_kb(couriers))


@dp.callback_query(F.data.startswith("cour|"))
async def courier_menu(call: types.CallbackQuery):
    courier_id = int(call.data.split("|")[-1])
    courier = await db.get_courier(courier_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'<b>Статистика #<code>{courier_id}</code>:</b>\n\n'
                              f'<b>Замовлень доставлено:</b> {courier["orders_completed"]}\n'
                              f'<b>Зароблено:</b> {courier["earned"]}',
                              reply_markup=courier_kb(courier_id))


@dp.callback_query(F.data.startswith("fire|"))
async def courier_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    courier_id = int(call.data.split("|")[-1])
    await call.message.answer(f"Звільнити кур'єра #{courier_id} ?", reply_markup=fire_courier(courier_id))
    await state.set_state(CourierDelete.q1)


@dp.callback_query(F.data.startswith("cfire|"), CourierDelete.q1)
async def courier_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    courier_id = int(call.data.split("|")[-1])
    await db.delete_courier(courier_id)

    couriers = await db.get_couriers()
    await call.message.answer("Кур'єра звільнено 😎", reply_markup=couriers_kb(couriers))
    await state.clear()


@dp.callback_query(F.data == 'addcour')
async def courier_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Введіть TG-Айді кур'єра:", reply_markup=cancel_add_courier())
    await state.set_state(CourierAdd.CourierId.q1)


@dp.message(F.text.isdigit(), CourierAdd.CourierId.q1)
async def courier_menu(message: types.Message, state: FSMContext):
    courier_id = int(message.text)
    await state.set_data({'q1':courier_id})
    await message.answer(f"Додаємо кур'єра #{courier_id} ?", reply_markup=add_courier(courier_id))
    await state.set_state(CourierAdd.Confirm.q1)


@dp.callback_query(F.data.startswith("cadd|"), CourierAdd.Confirm.q1)
async def courier_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    data = await state.get_data()
    courier_id = data['q1']
    await db.add_courier(courier_id)
    couriers = await db.get_couriers()
    await call.message.answer(f"Кур'єр #{courier_id} успішно доданий!", reply_markup=couriers_kb(couriers))
    await state.clear()


@dp.callback_query(F.data == 'back_to_couriers')
async def courier_menu(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state():
        await state.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    couriers = await db.get_couriers()
    await call.message.answer("Кур'єри", reply_markup=couriers_kb(couriers))