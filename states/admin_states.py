from aiogram.fsm.state import StatesGroup, State


"""GOODS AND CATEGORIES"""


class ChangeGood(StatesGroup):
    class Name(StatesGroup):
        q1 = State()

    class Description(StatesGroup):
        q1 = State()

    class Amount(StatesGroup):
        q1 = State()

    class Price(StatesGroup):
        q1 = State()

    class Delete(StatesGroup):
        q1 = State()


class CreateGood(StatesGroup):
    class Name(StatesGroup):
        q1 = State()

    class Description(StatesGroup):
        q1 = State()

    class Amount(StatesGroup):
        q1 = State()

    class Price(StatesGroup):
        q1 = State()

    class Confirm(StatesGroup):
        q1 = State()


class ChangeCategory(StatesGroup):
    class Name(StatesGroup):
        q1 = State()

    class Delete(StatesGroup):
        q1 = State()


class CreateCategory(StatesGroup):
    class Name(StatesGroup):
        q1 = State()

    class Confirm(StatesGroup):
        q1 = State()


"""COURIERS"""


class CourierAdd(StatesGroup):
    class CourierId(StatesGroup):
        q1 = State()

    class Confirm(StatesGroup):
        q1 = State()


class CourierDelete(StatesGroup):
    q1 = State()


"""SEND"""


class AddInfoStates(StatesGroup):
    text = State()
    buttons = State()
    confirm = State()


"""SETTINGS"""


class Settings(StatesGroup):
    class Time(StatesGroup):
        q1 = State()
        q2 = State()

    class Price(StatesGroup):
        q1 = State()
        q2 = State()


"""ORDERS"""


class DeleteOrder(StatesGroup):
    q1 = State()

