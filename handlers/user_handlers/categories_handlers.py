from aiogram import F
from loader import dp, db, bot
from keyboards.keyboards import *
from states.states import ChoseAmount
from aiogram.fsm.context import FSMContext
from utils.some_shit import user_pagination


@dp.callback_query(F.data.startswith('cat|'))
async def show_cat(call: types.CallbackQuery):
    cat, cat_id = call.data.split('|')
    goods = await db.get_goods_by_category_id(int(cat_id))
    cat_name = await db.get_category_by_category_id(int(cat_id))

    #PAGINATION
    max_items_per_page = 10
    user_pagination[call.message.chat.id] = 0  # Setting page to 0
    print(user_pagination[call.message.chat.id])

    start = user_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
    end = start + max_items_per_page  # END INDEX

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f"<b>{cat_name['category_name']}</b>", reply_markup=catalog_goods(goods[start:end], cat_id))


@dp.callback_query(F.data.startswith("good|"))
async def show_good(call: types.CallbackQuery):
    good, good_id = call.data.split("|")
    good = await db.get_good_by_good_id(int(good_id))
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'<b>{good["good_name"]}</b>'
                              f'\n\n📝Опис: {good["description"]}'
                              f'\n\n💸Ціна:{good["price"]}'
                              f'\n\nВ наявності: {good["amount"]}',
                              reply_markup=good_kb(good['good_id'], good['category_id'], available=True if good['amount'] > 0 else False))


@dp.callback_query(F.data.startswith("add_to|"))
async def add_to_bucket(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    add_to, good_id = call.data.split("|")
    bucket = await db.get_bucket(call.message.chat.id)
    if bucket['bucket'] is not None:
        for items in bucket['bucket']:
            if int(good_id) in items:
                await call.message.answer('У вас є вже цей товар в кошику!', reply_markup=menu(call.message.chat.id))
                return
            else:
                pass

    good = await db.get_good_by_good_id(int(good_id))
    await call.message.answer(f'Яку кількість ви бажаєте замовити?\nДоступно: {good["amount"]}',
                              reply_markup=cancel_amount(good['category_id']))
    await state.set_data({'q1': [good['amount'], int(good_id)]})
    await state.set_state(ChoseAmount.q1)


@dp.message(F.text.isnumeric(), ChoseAmount.q1)
async def get_good_amount(message: types.Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    total_amount = data['q1'][0]
    good_id = data['q1'][1]
    good = await db.get_good_by_good_id(int(good_id))
    cat_id = good['category_id']

    if amount > total_amount:
        await message.answer('Кількість недоступна. Введіть іншу кількість!', reply_markup=cancel_amount(good['category_id']))
        return
    else:
        await db.add_good_to_bucket(cat_id, good_id, amount, message.chat.id)
        # await db.subtract_amount_goods(good_id, amount)
        await state.clear()
        await message.answer('Додано до кошику!', reply_markup=menu(message.chat.id))


@dp.callback_query(F.data.startswith("page"))
async def next_page(call: types.CallbackQuery):
    cmd, action, cat_id = call.data.split('|')
    goods = await db.get_goods_by_category_id(int(cat_id))

    goods_number = len(goods)
    max_items_per_page = 10

    # Checking if user is in dict
    if call.message.chat.id not in user_pagination:
        user_pagination[call.message.chat.id] = 0  # If NOT -> setting the page

    if action == 'next':
        user_pagination[call.message.chat.id] += 1  # Adding 1 page
    else:
        user_pagination[call.message.chat.id] -= 1  # Subtracting 1 page

    # Checking if the page is not last
    if action == 'next':
        if user_pagination[call.message.chat.id]*max_items_per_page > goods_number:
            user_pagination[call.message.chat.id] -= 1  # subtracting 1 page
            await call.answer('Ви на останній сторінці')
        else:
            start = user_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
            end = start+max_items_per_page  # END INDEX
            goods = goods[start:end]
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=catalog_goods(goods, int(cat_id)))
    else:
        if user_pagination[call.message.chat.id] < 0:
            await call.answer('Ви на першій сторінці')
            user_pagination[call.message.chat.id] = 0
        else:
            start = user_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
            end = start + max_items_per_page  # END INDEX
            goods = goods[start:end]
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=catalog_goods(goods, int(cat_id)))


@dp.callback_query(F.data == 'back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Назад: ', reply_markup=menu(call.message.chat.id))


@dp.callback_query(F.data == 'back_to_categories')
async def back_to_menu(call: types.CallbackQuery):
    categories = await db.get_all_categories()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Каталог: ', reply_markup=catalog_categories(categories))


@dp.callback_query(F.data.startswith('back_to_goods|'))
async def back_to_goods(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    cat_id = call.data.split("|")[-1]
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    goods = await db.get_goods_by_category_id(int(cat_id))
    cat = await db.get_category_by_category_id(int(cat_id))
    cat_name = cat['category_name']

    max_items_per_page = 10
    try:
        start = user_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
    except KeyError:
        start = 0 * max_items_per_page  # START INDEX

    end = start + max_items_per_page  # END INDEX
    goods = goods[start:end]
    await call.message.answer(f'<b>{cat_name}:</b> ', reply_markup=catalog_goods(goods, cat_id))
