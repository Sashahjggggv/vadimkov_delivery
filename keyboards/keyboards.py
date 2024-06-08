from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config.cfg import admins


def catalog_categories(categories):
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(
            types.InlineKeyboardButton(text=category["category_name"], callback_data=f'cat|{category["category_id"]}'))
    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_to_menu'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def catalog_goods(goods, category_id):
    builder_list = InlineKeyboardBuilder()

    for good in goods:
        builder_list.add(
            types.InlineKeyboardButton(text=good["good_name"], callback_data=f'good|{good["good_id"]}'))
    builder_list.adjust(2)

    builder_pagination = InlineKeyboardBuilder()
    builder_pagination.row(
        types.InlineKeyboardButton(text='<<<', callback_data=f'page|prev|{category_id}'),
        types.InlineKeyboardButton(text='>>>', callback_data=f'page|next|{category_id}'))

    builder_pagination.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_to_categories'))
    builder_pagination.adjust(2)

    builder_list.attach(builder_pagination)

    keyboard = builder_list.as_markup(resize_keyboard=True)
    return keyboard


def good_kb(good_id, cat_id, available):
    builder = InlineKeyboardBuilder()

    if available is True:
        builder.add(
            types.InlineKeyboardButton(text='🛒 Додати в кошик', callback_data=f'add_to|{good_id}')
        )
    else:
        builder.add(
            types.InlineKeyboardButton(text='❌ Немає в наявності', callback_data=f'-')
        )
    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'back_to_goods|{cat_id}')
    )

    builder.adjust(1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def cancel_amount(cat_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text='Назад ◀️', callback_data=f'back_to_goods|{cat_id}')
    )
    builder.adjust(1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard



def pay_delivery():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text='📝 Оформити замовлення', callback_data='pay_delivery')
    )
    builder.add(
        types.InlineKeyboardButton(text='🗑 Очистити кошик', callback_data='clear_bucket')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def menu(user_id=0):
    builder = ReplyKeyboardBuilder()

    builder.add(
        types.KeyboardButton(text='🛒 Каталог'),
    )

    builder.add(
        types.KeyboardButton(text='⚡️ Кошик'),
    )

    builder.add(
        types.KeyboardButton(text='👤 Профіль'),
    )

    if user_id in admins:
        builder.add(
            types.KeyboardButton(text='⚙️ Адмінка'),
        )

    builder.adjust(2, 1, 1)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def change_values():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='Змінити адресу', callback_data='change_address'),
        types.InlineKeyboardButton(text='Змінити контактні данні', callback_data='change_contact')
    )
    builder.add(
        types.InlineKeyboardButton(text='Змінити коментар', callback_data='change_comment')
    )
    builder.row(
        types.InlineKeyboardButton(text='✅', callback_data='confirm_delivery'),
        types.InlineKeyboardButton(text='❌', callback_data='cancel_delivery')
    )

    builder.adjust(2, 1, 2)

    keyboard = builder.as_markup()
    return keyboard


def cancel_delivery(comment=False):
    builder = InlineKeyboardBuilder()

    if comment is not False:
        builder.add(
            types.InlineKeyboardButton(text='Без коментарів', callback_data='no_comments')
        )

    builder.add(
        types.InlineKeyboardButton(text='❌ Відмінити', callback_data='cancel_delivery')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def orders_list(orders):
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.add(
            types.InlineKeyboardButton(text=f"#{order['order_id']}", callback_data=f'o|{order["order_id"]}')
        )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def profile_back_list():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text=f"Назад ◀️", callback_data=f'back_to_profile_list')
    )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def courier_kb(courier_id, order_id, user_id=False, delivering=False):
    builder = InlineKeyboardBuilder()

    if delivering is False:
        builder.add(
            types.InlineKeyboardButton(text='Взяти замовлення', callback_data=f't|{courier_id}|{order_id}')
        )
    else:
        builder.add(
            types.InlineKeyboardButton(text='Доставлено', callback_data=f'd|{courier_id}|{order_id}')
        )

    if user_id is not False:
        builder.add(
            types.InlineKeyboardButton(text='Телеграм клієнта', callback_data='user', url=f'tg://user?id={user_id}')
        )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def admin_order_notify(courier_id):
    builder = InlineKeyboardBuilder()
    try:
        builder.add(
            types.InlineKeyboardButton(text="Телеграм кур'єра", callback_data='user', url=f'tg://user?id={courier_id}')
        )
    except (Exception,):
        pass

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def profile_orders_list(orders):
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.add(
            types.InlineKeyboardButton(text=f"#{order['order_id']}", callback_data=f'po|{order["order_id"]}')
        )

    builder.adjust(3)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def check_pay(user_id, order_id):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text='✅ Відправити замовлення', callback_data=f'c|{user_id}|{order_id}')
    )

    builder.add(
        types.InlineKeyboardButton(text='❌ Видалити заявку', callback_data='cancel_delivery')
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


def profile_back():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text=f"Назад ◀️", callback_data=f'back_to_profile')
    )

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


