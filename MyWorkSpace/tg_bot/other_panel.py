from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext

from States import User
from TRASH.label_list import bot, dp
from sql_telega import Database


@dp.message_handler(commands='start', state=None)
async def start_chat(message: types.message):
    if Database().user_found(message.from_user.id):
        await User.step_3.set()
    else:
        Database().add_user("null", "null", message.from_user.username, date.today(), False, message.from_user.id)
        await bot.send_message(message.chat.id, "Вы зарегистрировались:")
        await User.step_1.set()


@dp.message_handler(commands=["stop_bot"], state=User.step_3)
async def help_info(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Вы вышли из профиля!")
    await state.finish()


# @dp.message_handler(state=User.step_1)
# async def start(message: types.Message, state: FSMContext):
#     name = Database().user_info(message.from_user.username)
#     useradd = f"{name[0][0]}, {name[0][1]}, {name[0][2]}\n"
#     await message.reply("Для полной информации о командах введите /help  \nВы вошли под пользователем  " + useradd)
#     await User.step_3.set()


@dp.message_handler(commands=["help", "h"], state=User.step_3)
async def help_info(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "/help - Информация о коммандах\n"
                                            "/stop_bot - Завершить работу\n")
