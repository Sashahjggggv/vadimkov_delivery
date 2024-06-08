import types
from loader import dp, db, bot, rt
from aiogram.filters import Command, CommandObject, BaseFilter
from keyboards.admin_keyboards import *
from aiogram import F
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import menu
from utils.some_shit import admin_pagination
from states.admin_states import *
from utils.some_shit import IsAdmin


@dp.message(IsAdmin(), F.text == '⚙️ Адмінка')
async def admin_menu(message: types.Message):
    await message.answer('Адмінка:', reply_markup=admin_kb())


@dp.message(F.text == 'Налаштування товару', IsAdmin())
async def admin_goods(message: types.Message):
    categories = await db.get_all_categories()
    await message.answer('Виберіть товар: ', reply_markup=admin_catalog_categories(categories))


@dp.callback_query(F.data.startswith('cad|'), IsAdmin())
async def admin_goods(call: types.CallbackQuery):
    cad, category_id = call.data.split("|")
    goods = await db.get_goods_by_category_id(int(category_id))

    # PAGINATION
    max_items_per_page = 10
    admin_pagination[call.message.chat.id] = 0  # Setting page to 0

    start = admin_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
    end = start + max_items_per_page  # END INDEX

    await bot.edit_message_reply_markup(call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=admin_catalog_goods(goods=goods[start:end],
                                                                         category_id=category_id))


@dp.callback_query(F.data.startswith("gad|"), IsAdmin())
async def show_good(call: types.CallbackQuery):
    good, good_id = call.data.split("|")
    good = await db.get_good_by_good_id(int(good_id))
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'<b>{good["good_name"]}</b>'
                              f'\n\n📝Опис: {good["description"]}'
                              f'\n\n💸Ціна:{good["price"]}'
                              f'\n\nВ наявності: {good["amount"]}',
                              reply_markup=admin_good_kb(good['good_id'], good['category_id']))


@dp.callback_query(F.data.startswith("cn|"), IsAdmin())
async def cn_good(call: types.CallbackQuery, state: FSMContext):
    cn, good_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть нову назву товару: ', reply_markup=cancel_good_change(good_id))
    await state.set_state(ChangeGood.Name.q1)
    await state.update_data({'q1': int(good_id)})


@dp.message(F.text, ChangeGood.Name.q1)
async def cn_good(message: types.Message, state: FSMContext):
    data = await state.get_data()
    good_id = int(data['q1'])
    await db.change_good_name(good_id, message.text)

    good = await db.get_good_by_good_id(int(good_id))
    await message.answer('Назва товару змінена.')
    await message.answer(f'<b>{good["good_name"]}</b>'
                         f'\n\n📝Опис: {good["description"]}'
                         f'\n\n💸Ціна:{good["price"]}'
                         f'\n\nВ наявності: {good["amount"]}',
                         reply_markup=admin_good_kb(good['good_id'], good['category_id']))
    await state.clear()


@dp.callback_query(F.data.startswith('cd|'))
async def cd_good(call: types.CallbackQuery, state: FSMContext):
    cd, good_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть новий опис товару: ', reply_markup=cancel_good_change(good_id))
    await state.set_state(ChangeGood.Description.q1)
    await state.update_data({'q1': int(good_id)})


@dp.message(F.text, ChangeGood.Description.q1)
async def cd_good(message: types.Message, state: FSMContext):
    data = await state.get_data()
    good_id = int(data['q1'])
    await db.change_good_description(good_id, message.text)

    good = await db.get_good_by_good_id(int(good_id))
    await message.answer('Опис товару змінений.')
    await message.answer(f'<b>{good["good_name"]}</b>'
                         f'\n\n📝Опис: {good["description"]}'
                         f'\n\n💸Ціна:{good["price"]}'
                         f'\n\nВ наявності: {good["amount"]}',
                         reply_markup=admin_good_kb(good['good_id'], good['category_id']))
    await state.clear()


@dp.callback_query(F.data.startswith('cp|'))
async def cp_good(call: types.CallbackQuery, state: FSMContext):
    cd, good_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть нову ціну товару: ', reply_markup=cancel_good_change(good_id))
    await state.set_state(ChangeGood.Price.q1)
    await state.update_data({'q1': int(good_id)})


@dp.message(F.text.isnumeric(), ChangeGood.Price.q1)
async def cp_good(message: types.Message, state: FSMContext):
    data = await state.get_data()
    good_id = int(data['q1'])
    await db.change_good_price(good_id, int(message.text))

    good = await db.get_good_by_good_id(int(good_id))
    await message.answer('Ціна товару змінена.')
    await message.answer(f'<b>{good["good_name"]}</b>'
                         f'\n\n📝Опис: {good["description"]}'
                         f'\n\n💸Ціна:{good["price"]}'
                         f'\n\nВ наявності: {good["amount"]}',
                         reply_markup=admin_good_kb(good['good_id'], good['category_id']))
    await state.clear()


@dp.message(F.text, ChangeGood.Price.q1)
async def cp_good(message: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await message.answer('Введіть ціну числом.', reply_markup=cancel_good_change(data['q1']))
    return


@dp.callback_query(F.data.startswith('ca|'))
async def cp_good(call: types.CallbackQuery, state: FSMContext):
    cd, good_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть нову кілкість товару: ', reply_markup=cancel_good_change(good_id))
    await state.set_state(ChangeGood.Amount.q1)
    await state.update_data({'q1': int(good_id)})


@dp.message(F.text.isnumeric(), ChangeGood.Amount.q1)
async def cp_good(message: types.Message, state: FSMContext):
    data = await state.get_data()
    good_id = int(data['q1'])
    await db.change_good_amount(good_id, int(message.text))

    good = await db.get_good_by_good_id(int(good_id))
    await message.answer('Ціна товару змінена.')
    await message.answer(f'<b>{good["good_name"]}</b>'
                         f'\n\n📝Опис: {good["description"]}'
                         f'\n\n💸Ціна:{good["price"]}'
                         f'\n\nВ наявності: {good["amount"]}',
                         reply_markup=admin_good_kb(good['good_id'], good['category_id']))
    await state.clear()


@dp.message(F.text, ChangeGood.Amount.q1)
async def cp_good(message: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await message.answer('Введіть кількість числом.', reply_markup=cancel_good_change(data['q1']))
    return


@dp.callback_query(F.data.startswith("del|"))
async def del_good(call: types.CallbackQuery, state: FSMContext):
    delete, good_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Підтвердіть видалення', reply_markup=delete_good_kb(good_id))
    await state.set_state(ChangeGood.Delete.q1)
    await state.update_data({'q1': int(good_id)})


@dp.callback_query(F.data.startswith('cdel|'), ChangeGood.Delete.q1)
async def del_good(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    cdel, good_id = call.data.split("|")
    good = await db.get_good_by_good_id(int(good_id))
    category_id = good['category_id']
    await db.delete_good(int(good_id))
    await call.message.answer('Товар видалений.')

    goods = await db.get_goods_by_category_id(int(category_id))

    # PAGINATION
    max_items_per_page = 10
    admin_pagination[call.message.chat.id] = 0  # Setting page to 0

    start = admin_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
    end = start + max_items_per_page  # END INDEX

    await call.message.answer('Товари:', reply_markup=admin_catalog_goods(goods=goods[start:end],
                                                                          category_id=category_id))
    await state.clear()


@dp.callback_query(F.data.startswith('adm_back_to_goods|'))
async def back_to_goods(call: types.CallbackQuery, state: FSMContext):
    cad, category_id = call.data.split("|")
    goods = await db.get_goods_by_category_id(int(category_id))
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    # PAGINATION
    max_items_per_page = 10
    admin_pagination[call.message.chat.id] = 0  # Setting page to 0

    start = admin_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
    end = start + max_items_per_page  # END INDEX

    await call.message.answer('Товари: ', reply_markup=admin_catalog_goods(goods=goods[start:end],
                                                                           category_id=category_id))


@dp.callback_query(F.data.startswith('cancel_gc|'))
async def change_good_cancel(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    cancel, good_id = call.data.split("|")
    good = await db.get_good_by_good_id(int(good_id))
    await call.message.answer('Відміна.')
    await call.message.answer(f'<b>{good["good_name"]}</b>'
                              f'\n\n📝Опис: {good["description"]}'
                              f'\n\n💸Ціна:{good["price"]}'
                              f'\n\nВ наявності: {good["amount"]}',
                              reply_markup=admin_good_kb(good['good_id'], good['category_id']))
    await state.clear()


@dp.callback_query(F.data.startswith("addgood|"))
async def add_good(call: types.CallbackQuery, state: FSMContext):
    addgood, category_id = call.data.split("|")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть назву нового товару: ', reply_markup=cancel_creation_good(category_id))
    await state.set_state(CreateGood.Name.q1)
    await state.set_data({'q1':[int(category_id)]})


@dp.message(F.text, CreateGood.Name.q1)
async def add_good_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'q1': [data['q1'], message.text]})
    await state.set_state(CreateGood.Description.q1)
    await message.answer('Введіть опис нового товару: ', reply_markup=cancel_creation_good(data['q1'][0]))


@dp.message(F.text, CreateGood.Description.q1)
async def add_good_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'q2': message.text})
    await state.set_state(CreateGood.Price.q1)
    await message.answer('Введіть ціну нового товару: ', reply_markup=cancel_creation_good(data['q1'][0]))


@dp.message(F.text.isnumeric(), CreateGood.Price.q1)
async def add_good_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'q3': int(message.text)})
    await state.set_state(CreateGood.Amount.q1)
    await message.answer('Введіть кількість нового товару: ', reply_markup=cancel_creation_good(data['q1'][0]))


@dp.message(F.text, CreateGood.Price.q1)
async def add_good_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Введіть ціну числом.', reply_markup=cancel_creation_good(data['q1'][0]))
    return


@dp.message(F.text.isnumeric(), CreateGood.Amount.q1)
async def add_good_amount(message: types.Message, state: FSMContext):
    await state.update_data({'q4': int(message.text)})
    await state.set_state(CreateGood.Confirm.q1)
    await add_good_final(message, state)


@dp.message(F.text, CreateGood.Amount.q1)
async def add_good_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Введіть кількість числом.', reply_markup=cancel_creation_good(data['q1'][0]))
    return


@dp.message(F.text.isnumeric(), CreateGood.Amount.q1)
async def add_good_final(message: types.Message, state: FSMContext):
    await state.update_data({'q4': int(message.text)})
    await state.set_state(CreateGood.Confirm.q1)
    data = await state.get_data()
    await message.answer(f'<b>{data["q1"][-1]}</b>'
                          f'\n\n📝Опис: {data["q2"]}'
                          f'\n\n💸Ціна:{data["q3"]}'
                          f'\n\nВ наявності: {data["q4"]}', reply_markup=confirm_creation_good(data['q1'][0]))


@dp.callback_query(F.data.startswith("c_good|"), CreateGood.Confirm.q1)
async def confirm_good(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await db.add_good(name=data['q1'][-1],
                      description=data['q2'],
                      price=int(data['q3']),
                      amount=int(data['q4']),
                      category_id=int(data['q1'][0][0]))
    await call.message.answer('Товар доданий!', reply_markup=admin_kb())
    await state.clear()


@dp.callback_query(F.data.startswith("cancel_creation|"))
async def cancel_c(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Відміна', reply_markup=admin_kb())


@dp.callback_query(F.data == 'back_to_adm_categories')
async def back_to_adm_categories(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    categories = await db.get_all_categories()
    await call.message.answer("Виберіть категорію", reply_markup=admin_catalog_categories(categories))


@dp.message(F.text == 'Налаштування категорій', IsAdmin())
async def categories_settings(message: types.Message):
    categories = await db.get_all_categories()
    await message.answer("Виберіть категорію", reply_markup=admin_create_categories(categories))


@dp.callback_query(F.data.startswith("cad_ch|"))
async def creation_good(call: types.CallbackQuery):
    cad_ch, cat_id = call.data.split("|")
    category = await db.get_category_by_category_id(int(cat_id))
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'{category["category_name"]}', reply_markup=admin_category_kb(cat_id))


@dp.callback_query(F.data.startswith("catname|"), IsAdmin())
async def chname_catalog(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    catname, cat_id = call.data.split("|")
    await call.message.answer("Введіть нову назву категорії", reply_markup=cancel_creation_good(cat_id))
    await state.set_state(ChangeCategory.Name.q1)
    await state.set_data({"q1": int(cat_id)})


@dp.message(F.text, ChangeCategory.Name.q1, IsAdmin())
async def chname_catalog(message: types.Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    await db.change_category_name(name=new_name,
                                  cat_id=data['q1'])
    await message.answer('Назва змінена!', reply_markup=admin_kb())
    await state.clear()


@dp.callback_query(F.data.startswith("delcat|"), IsAdmin())
async def delete_category(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    cat_id = int(call.data.split("|")[-1])
    category = await db.get_category_by_category_id(cat_id)
    await call.message.answer(f'Видаляємо <b>{category["category_name"]}?</b>\n'
                              f'Разом з категоріями також будуть видалені товари.', reply_markup=delete_category_kb(cat_id))
    await state.set_state(ChangeCategory.Delete.q1)
    await state.set_data({"q1": cat_id})


@dp.callback_query(F.data.startswith("catdel"))
async def delete_category(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    data = await state.get_data()
    await db.delete_category(data['q1'])
    await call.message.answer('Категорія видалена!', reply_markup=admin_kb())
    await state.clear()


@dp.callback_query(F.data.startswith("cancel_cc|"))
async def cancel_changes_cat(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Відміна', reply_markup=admin_kb())


@dp.callback_query(F.data == 'addcat', IsAdmin())
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Введіть назву категорії.', reply_markup=cancel_creation_category())
    await state.set_state(CreateCategory.Name.q1)


@dp.message(F.text, CreateCategory.Name.q1)
async def add_category(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(f'Додаємо категорію з назвою <b>{name}</b>?', reply_markup=confirm_c_creation())
    await state.set_data({'q1': name})
    await state.set_state(CreateCategory.Confirm.q1)


@dp.callback_query(F.data == 'create_c')
async def add_category(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.add_category(data['q1'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Категорія додана', reply_markup=admin_kb())
    await state.clear()


@dp.callback_query(F.data == 'cancel_c_creation')
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Відміна', reply_markup=admin_kb())
    await state.clear()


@dp.callback_query(F.data == 'back_to_cat_list')
async def back_to_cat_list(call: types.CallbackQuery):
    categories = await db.get_all_categories()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Категорії', reply_markup=admin_create_categories(categories))


@dp.callback_query(F.data.startswith("apage"), IsAdmin())
async def adm_pagination(call: types.CallbackQuery):
    cmd, action, cat_id = call.data.split('|')
    goods = await db.get_goods_by_category_id(int(cat_id))

    goods_number = len(goods)
    max_items_per_page = 10

    # Checking if user is in dict
    if call.message.chat.id not in admin_pagination:
        admin_pagination[call.message.chat.id] = 0  # If NOT -> setting the page

    if action == 'next':
        admin_pagination[call.message.chat.id] += 1  # Adding 1 page
    else:
        admin_pagination[call.message.chat.id] -= 1  # Subtracting 1 page

    # Checking if the page is not last
    if action == 'next':
        if admin_pagination[call.message.chat.id] * max_items_per_page > goods_number:
            admin_pagination[call.message.chat.id] -= 1  # subtracting 1 page
            await call.answer('Ви на останній сторінці')
        else:
            start = admin_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
            end = start + max_items_per_page  # END INDEX
            goods = goods[start:end]
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=admin_catalog_goods(goods, int(cat_id)))
    else:
        if admin_pagination[call.message.chat.id] < 0:
            await call.answer('Ви на першій сторінці')
            admin_pagination[call.message.chat.id] = 0
        else:
            start = admin_pagination[call.message.chat.id] * max_items_per_page  # START INDEX
            end = start + max_items_per_page  # END INDEX
            goods = goods[start:end]
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=admin_catalog_goods(goods, int(cat_id)))


@dp.message(F.text == 'В меню')
async def to_menu(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
    await message.answer('Меню', reply_markup=menu(message.chat.id))
"""
+Додавати/Видаляти/Змінювати Категорії/Товар
+Додавати-Видаляти кур'єрів
+Розсилка
+Статистика
+Змінювати робочий час
+Змінювати ціну доставки
+Повідомити про закінчення товару

+Доробити кнопку назад в каталозі
"""
