from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage

from States import Admin, User
from TRASH.label_list import bot, dp
from sql_telega import Database


@dp.message_handler(user_id=Database().list_admin(), commands='admin', state=User.step_3)
async def start_chat(message: types.message):
    if Database().user_found(message.from_user.id):
        await bot.send_message(message.chat.id, "Введите ваш логин:")
        await Admin.registration_login.set()
    else:
        await bot.send_message(message.chat.id, "Вы не зарегестрированы, \nВведите ваш логин для входа:")
        await Admin.registration_login.set()


@dp.message_handler(user_id=Database().list_admin(), state=Admin.registration_login)
async def registration_start(message: types.Message, state: FSMContext):
    if Database().user_found(message.from_user.id):
        login = message.text
        if Database().user_log(message.text, message.from_user.id):
            await bot.send_message(message.chat.id, "Введите ваш пароль:")
            await Admin.registration_pass.set()
        else:
            await bot.send_message(message.chat.id, f"Пароль был введен неверно.")
    else:
        login = message.text
        async with state.proxy() as data:
            data['login'] = login
        await bot.send_message(message.chat.id, "Введите ваш пароль для пользователя:")
        await Admin.registration_pass.set()


@dp.message_handler(user_id=Database().list_admin(), state=Admin.registration_pass)
async def registration_start(message: types.Message, state: FSMContext):
    if Database().user_found(message.from_user.id):
        if Database().user_pass(message.text, message.from_user.id):
            await bot.send_message(message.chat.id,
                                   "Авторизация прошла успешно \nДля информации пропишите /h или /help")
            await Admin.step_3.set()
        else:
            await bot.send_message(message.chat.id, f"Пароль был введен неверно.")
    else:
        async with state.proxy() as data:
            login = data['login']
            password = message.text
            Database().update_user(login, password, message.from_user.id)
            await bot.send_message(message.chat.id, "Введите /start и авторизуйтесь снова:")
            await Admin.step_3.set()


# Сделать назначение пользователю вебхук, и прописать последовательность
@dp.message_handler(user_id=Database().list_admin(), state=Admin.step_1)
async def start(message: types.Message, state: FSMContext):
    name = Database().user_info(message.from_user.username)
    useradd = f"{name[0][0]}, {name[0][1]}, {name[0][2]}\n"

    await message.reply("Для полной информации о командах введите /help  \nВы вошли под пользователем  " + useradd)
    await Admin.step_3.set()


@dp.message_handler(user_id=Database().list_admin(), commands=["help", "h"], state=Admin.step_3)
async def help_info(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "/help - Информация о коммандах\n"
                                            "/delete_user - удалить юзера из бд \n"
                                            "/delete_hook - удалить юзера из бд \n"
                                            "/set_hook - удалить юзера из бд \n"
                                            "/stop_bot - остановить бота\n"
                                            "/ALL - информация о зарегестрированных юзерах")


@dp.message_handler(user_id=Database().list_admin(), commands=["set_hook"], state=Admin.step_3)
async def hook_start(message: types.Message, state: FSMContext):
    name = Database().show_users()
    useradd = ""
    for information in name:
        useradd += f"{information[0]}, {information[1]}, {information[2]},{information[3]}\n"
    await bot.send_message(message.chat.id,
                           "Выберите пользователя из списка и напишите название hook-a\n" + useradd + "\nВведите STOP для отмены")
    await Admin.set_hook.set()

@dp.message_handler(user_id=Database().list_admin(), commands=["delete_hook"], state=Admin.step_3)
async def hook_delete(message: types.Message, state: FSMContext):
    name = Database().show_users()
    useradd = ""
    for information in name:
        useradd += f"{information[0]}, {information[1]}, {information[2]},{information[3]}\n"
    await bot.send_message(message.chat.id,
                           "Выберите пользователя из списка и напишите название hook-a для удаления\n" + useradd + "\nВведите STOP для отмены")
    await Admin.delete_hook.set()
@dp.message_handler(user_id=Database().list_admin(), state=Admin.set_hook)
async def hook_work(message: types.Message, state: FSMContext):
    if message.text.lower() == "stop":
        await bot.send_message(message.chat.id, "/help - Информация о коммандах\n"
                                                "/delete_user - удалить юзера из бд \n"
                                                "/delete_hook - удалить юзера из бд \n"
                                                "/set_hook - удалить юзера из бд \n"
                                                "/stop_bot - остановить бота\n"
                                                "/ALL - информация о зарегестрированных юзерах")
        await Admin.step_3.set()
    else:
        text = message.text.replace(" ", "").split(",")
        if len(text) == 2:
            if Database().user_id_found(text[0]):
                Database().set_web(text[1])
                await Admin.step_3.set()
            else:
                await bot.send_message(message.chat.id, "id не был найден")
        else:
            await bot.send_message(message.chat.id, "Неверно введено сообщение пример: id, hook_name")

@dp.message_handler(user_id=Database().list_admin(), state=Admin.delete_hook)
async def hook_reset(message: types.Message, state: FSMContext):
    if message.text.lower() == "stop":
        await bot.send_message(message.chat.id, "/help - Информация о коммандах\n"
                                                "/delete_user - удалить юзера из бд \n"
                                                "/delete_hook - удалить юзера из бд \n"
                                                "/set_hook - удалить юзера из бд \n"
                                                "/stop_bot - остановить бота\n"
                                                "/ALL - информация о зарегестрированных юзерах")
        await Admin.step_3.set()
    else:
        text = message.text.replace(" ", "").split(",")
        if len(text) == 2:
            if Database().user_id_found(text[0]):
                if Database().web_found(text[1]):
                    Database().delete_web(text[1])
                else:
                    await bot.send_message(message.chat.id, "web hook не был найден")
                await Admin.step_3.set()
            else:
                await bot.send_message(message.chat.id, "id не был найден")
        else:
            await bot.send_message(message.chat.id, "Неверно введено сообщение пример: id, hook_name")


@dp.message_handler(user_id=Database().list_admin(), commands=["stop_bot"], state=Admin.step_3)
async def help_info(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Вы вышли из профиля!")
    await state.finish()


@dp.message_handler(user_id=Database().list_admin(), commands="ALL", state=Admin.step_3)
async def start(message: types.Message, state: FSMContext):
    name = Database().show_users()
    useradd = ""
    for information in name:
        useradd += f"{information[0]}, {information[1]}, {information[2]},{information[3]},{information[7]}\n"
    await message.reply(useradd)


@dp.message_handler(user_id=Database().list_admin(), commands="delete_user", state=Admin.step_3)
async def delete_user(message: types.Message, state: FSMContext):
    name = Database().show_users()
    useradd = ""
    for information in name:
        useradd += f"{information[0]}, {information[1]}, {information[2]},{information[3]},{information[7]}\n"
    await bot.send_message(message.chat.id,
                           "Введите номер пользователя которого вы хочите удалить\n" + useradd + "\nВведите STOP для отмены")
    await Admin.delete_user.set()


@dp.message_handler(user_id=Database().list_admin(), state=Admin.delete_user)
async def delete_user(message: types.Message, state: FSMContext):
    if message.text.lower() == "stop":
        await bot.send_message(message.chat.id, "/help - Информация о коммандах\n"
                                                "/delete_user - удалить юзера из бд \n"
                                                "/delete_hook - удалить юзера из бд \n"
                                                "/set_hook - удалить юзера из бд \n"
                                                "/stop_bot - остановить бота\n"
                                                "/ALL - информация о зарегестрированных юзерах")
        await Admin.step_3.set()
    else:
        if Database().user_id_found(message.text):
            if Database().user_protect(message.text)[0]:
                await bot.send_message(message.chat.id,
                                       "Нельзя удалять админа")
                await Admin.step_3.set()
            else:
                Database().delete_user(message.text)
                await bot.send_message(message.chat.id, "Юзер удален")
                await Admin.step_3.set()
        else:
            await bot.send_message(message.chat.id, "Был введен неверный номер юзера")
            await Admin.step_3.set()


# @dp.message_handler(user_id=Database().list_admin(), commands="np", state=Admin.step_3)
# async def new_pass_1(message: types.Message, state: FSMContext):
#     await message.reply("Введите пароль: ")
#     await Admin.password_c.set()
