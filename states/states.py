from aiogram.fsm.state import StatesGroup, State


class ChoseAmount(StatesGroup):
    q1 = State()


class PayDelivery(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


PayDelivery_list = [PayDelivery.q1, PayDelivery.q2, PayDelivery.q3]

