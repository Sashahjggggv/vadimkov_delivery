from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def admin_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text='Налаштування товару'),
        types.KeyboardButton(text='Налаштування категорій')
    )
    builder.row(
        types.KeyboardButton(text="Налаштування бота"),
        types.KeyboardButton(text="Кур'єри")

    )
    builder.row(
        types.KeyboardButton(text="Статистика"),
    )
    builder.add(
        types.KeyboardButton(text="В меню")
    )

    builder.adjust(2, 2, 1, 1)
    keyboard = builder.as_markup(resize_keyboard=True)

    return keyboard


def admin_create_categories(categories):
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(
            types.InlineKeyboardButton(text=category["category_name"], callback_data=f'cad_ch|{category["category_id"]}'))

    builder_but = InlineKeyboardBuilder()
    builder_but.add(
        types.InlineKeyboardButton(text='Додати категорію ➕', callback_data='addcat')
    )
    # builder_but.add(
    #     types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_to_admin'))

    builder.adjust(2)
    builder_but.adjust(1)
    builder.attach(builder_but)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_catalog_categories(categories):
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(
            types.InlineKeyboardButton(text=category["category_name"], callback_data=f'cad|{category["category_id"]}'))
    # builder.add(
        # types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_to_admin'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_catalog_goods(goods, category_id):
    builder_list = InlineKeyboardBuilder()

    for good in goods:
        builder_list.add(
            types.InlineKeyboardButton(text=good["good_name"], callback_data=f'gad|{good["good_id"]}'))
    builder_list.adjust(2)

    builder_pagination = InlineKeyboardBuilder()
    builder_pagination.add(
        types.InlineKeyboardButton(text='Додати товар ➕', callback_data=f'addgood|{category_id}')
    )
    builder_pagination.row(
        types.InlineKeyboardButton(text='<<<', callback_data=f'apage|prev|{category_id}'),
        types.InlineKeyboardButton(text='>>>', callback_data=f'apage|next|{category_id}'))

    builder_pagination.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_to_adm_categories'))
    builder_pagination.adjust(1, 2, 1)

    builder_list.attach(builder_pagination)

    keyboard = builder_list.as_markup(resize_keyboard=True)
    return keyboard


def admin_good_kb(good_id, cat_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='Змінити назву', callback_data=f'cn|{good_id}'),
        types.InlineKeyboardButton(text='Змінити опис', callback_data=f'cd|{good_id}')
    )
    builder.add(
        types.InlineKeyboardButton(text='Змінити кількість', callback_data=f'ca|{good_id}'),
        types.InlineKeyboardButton(text='Змінити ціну', callback_data=f'cp|{good_id}'),
    )
    builder.add(
        types.InlineKeyboardButton(text='Видалити ❌', callback_data=f'del|{good_id}'),
    )
    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'adm_back_to_goods|{cat_id}')
    )

    builder.adjust(2, 2, 1, 1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_category_kb(cat_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='Змінити назву', callback_data=f'catname|{cat_id}'),
    )
    builder.add(
        types.InlineKeyboardButton(text='Видалити ❌', callback_data=f'delcat|{cat_id}'),
    )
    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'back_to_cat_list')
    )
    builder.adjust(1, 1, 1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_good_change(good_id):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'cancel_gc|{good_id}')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_category_change(cat_id):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'cancel_cc|{cat_id}')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def delete_category_kb(cat_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='✅', callback_data=f'catdel|{cat_id}'),
        types.InlineKeyboardButton(text='❌', callback_data=f'cancel_cc|{cat_id}')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def delete_good_kb(good_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='✅', callback_data=f'cdel|{good_id}'),
        types.InlineKeyboardButton(text='❌', callback_data=f'cancel_gc|{good_id}')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_creation_good(category_id):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'cancel_creation|{category_id}')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def confirm_creation_good(category_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='Додати', callback_data=f'c_good|{category_id}'),
        types.InlineKeyboardButton(text='Відміна', callback_data=f'cancel_creation|{category_id}')

    )

    keyboard = builder.as_markup()
    return keyboard


def confirm_c_creation():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='Додати', callback_data=f'create_c'),
        types.InlineKeyboardButton(text='Відміна', callback_data=f'cancel_c_creation')

    )

    keyboard = builder.as_markup()
    return keyboard


def cancel_creation_category():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'cancel_c_creation')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def couriers_kb(couriers):
    builder = InlineKeyboardBuilder()

    for courier in couriers:
        builder.add(
            types.InlineKeyboardButton(text=f"Кур'єр #{courier['id']}", callback_data=f'cour|{courier["id"]}')
        )

    builder_add = InlineKeyboardBuilder()
    builder_add.add(
        types.InlineKeyboardButton(text="Додати кур'єра ➕", callback_data=f'addcour')
    )
    builder_add.adjust(1)
    builder.adjust(2)
    builder.attach(builder_add)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def courier_kb(courier_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Звільнити кур'єра 👋", callback_data=f"fire|{courier_id}"),
        types.InlineKeyboardButton(text="ТГ Кур'єра", callback_data='tg', url=f'tg://user?id={courier_id}')
    )

    builder.add(
        types.InlineKeyboardButton(text="Назад ◀️", callback_data=f"back_to_couriers")
    )
    builder.adjust(2,1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_add_courier():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text="Назад ◀️", callback_data=f"back_to_couriers")
    )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def fire_courier(courier_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="Так ✅", callback_data=f"cfire|{courier_id}")
    )

    builder.add(
        types.InlineKeyboardButton(text="Ні ❌", callback_data=f"back_to_couriers")
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def add_courier(courier_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="Так ✅", callback_data=f"cadd|{courier_id}")
    )

    builder.add(
        types.InlineKeyboardButton(text="Ні ❌", callback_data=f"back_to_couriers")
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_send():
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text='Відміна')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def settings_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="Змінити час", callback_data=f"change_time")
    )

    builder.add(
        types.InlineKeyboardButton(text="Змінити ціну", callback_data=f"change_d_price")
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_settings():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text="Назад ◀️", callback_data=f"back_to_settings")
    )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_delete_order(order_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text=f"Видалити замовлення", callback_data=f'delo|{order_id}')
    )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_delete_o_confirm(order_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="✅", callback_data=f"cdelo|{order_id}")
    )

    builder.add(
        types.InlineKeyboardButton(text="❌", callback_data=f"cancel_delete")
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard