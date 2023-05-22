from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    registration_login = State()
    registration_pass = State()
    delete_user = State()
    delete_password = State()
    set_hook = State()
    delete_hook = State()


class User(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    registration_login = State()
    registration_pass = State()


text = "Hello, pitet"
print(text.replace(" ", "").split(","))
