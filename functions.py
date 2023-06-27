import os
from aiogram import types
from json import dumps, loads, load

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from create_bot import dp, bot
from db import Database

db = Database()
test = load(open("test.json", "r", encoding="utf-8"))
video = load(open("video.json", "r", encoding="utf-8"))


# отправка видео
async def video_send(link, user_id):
    video = YouTube(link)
    video_file_path = video.streams.get_highest_resolution().download()
    clip = VideoFileClip(video_file_path)
    width, height = clip.size
    filename = os.path.splitext(os.path.basename(clip.filename))[0]
    with open(video_file_path, 'rb') as video_file:
        await bot.send_video(chat_id=user_id, video=video_file,
                             width=width, height=height,
                             caption=filename)
    os.remove(video_file_path)


# хочешь начать тест?
async def prep_test_mess(user_id):
    knopka = InlineKeyboardMarkup()
    knopka.insert(InlineKeyboardButton("жми", callback_data="start_test"))
    msg = await bot.send_message(user_id, "Когда будешь готов начать тест, нажми на кнопку ниже", reply_markup=knopka)
    db.upd_msg(user_id, msg)


# составоение теста
def compose_markup(number: int, testing, d_exist):
    question = str(number)
    km = InlineKeyboardMarkup(row_width=3)
    cdA = {
        "question": number,
        "answer": "A"
    }
    km.insert(InlineKeyboardButton(testing[question]["A"], callback_data=dumps(cdA)))
    cdB = {
        "question": number,
        "answer": "B"
    }
    km.insert(InlineKeyboardButton(testing[question]["B"], callback_data=dumps(cdB)))
    cdC = {
        "question": number,
        "answer": "C"
    }
    km.insert(InlineKeyboardButton(testing[question]["C"], callback_data=dumps(cdC)))
    return km


@dp.callback_query_handler(lambda c: True)
async def answer_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = loads(callback.data)
    q = "test_" + str(data["question"])
    is_correct = test[q]["Correct"] == data["answer"]
    passed_value = db.get_passed(user_id)
    msg = db.get_msg(user_id)[0]
    if is_correct:
        passed = passed_value[0] + 1
        db.upd_passed(user_id, passed)
    if q == "test_25":
        score = db.get_passed(user_id)[0]
        if score <= 8:
            db.upd_level(user_id, "Beginner")
        elif score <= 12:
            db.upd_level(user_id, "Elementary")
        elif score <= 16:
            db.upd_level(user_id, "Pre-Intermediate")
        elif score <= 21:
            db.upd_level(user_id, "Intermediate")
        else:
            db.upd_level(user_id, "Upper-Intermediate")

        await bot.delete_message(callback.from_user.id, msg)
        await bot.send_message(callback.from_user.id, f"END.\n"
                                                      f"Your Score is {score}")
        return
    q = "test_" + str(data["question"] + 1)
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                text=test[q]["question_1"],
                                message_id=msg,
                                reply_markup=compose_markup(data["question"] + 1))


@dp.callback_query(text="start_test")
async def start_test(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if db.get_process(user_id)[0]:
        await bot.send_message(user_id,
                               "You are already doing test")
        return

    msg = db.get_msg(user_id)[0]
    await bot.delete_message(user_id, msg.message_id)  # удаления сообщения с кнопкой начала теста

    progress = db.get_leveling(user_id)[0]
    level = db.get_level(user_id)[0]
    testNumber = "test_" + video[level][progress]["test"]
    testing = test[level][testNumber]

    db.upd_process(user_id, True)
    d_exist = False

    if "D" in testing["1"].keys():
        d_exist = True

    msg = await bot.send_message(
        user_id,
        testing["1"],
        reply_markup=compose_markup(1, testing, d_exist)
    )
    db.upd_msg(user_id, msg.message_id)


# сообщение о конце обучения
async def end_mess(user_id, state: FSMContext):
    kb = [[types.KeyboardButton(text="Да")], [types.KeyboardButton(text="Нет")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="выберете вариант")
    coin = db.get_coin(user_id)
    await bot.send_message(user_id, f'Поздравляю это конец, ты набрал вот столько коинов: {coin}\n'
                                    f'Вот такие то у тебя скидки короче похуй')
    await bot.send_message(user_id,
                           f'Перед тем как я с тобой попрощаюсь навсегда хочу тебе предложить 1 вещь который возможно тебя заинтересует называется он NCF English и там ты сможешь быть самым лучшим в группе ведь у тебя есть преимущества в виде меня и от меня символический подарок, скидка поскольку я уважаю твой труд и время',
                           reply_markup=keyboard)
    await state.set_state('waiting')


@dp.message_handler(state='waiting')
async def interesting_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отправить контакт", request_contact=True))
    if message == 'Да':
        await bot.send_message(message.from_user.id,
                               "Рад видеть что у тебя есть рвение изучать язык дальше, напиши мне свои контактные данные (ФИО и номер телефона) я передам нашим специалистам они обязательно с тобой свяжутся",
                               reply_markup=keyboard)
        await state.set_state('wait_for_number')
    elif message == 'Нет':
        await bot.send_message(message.from_user.id,
                               'На нет и суда нет, это только твоё право, уверен что знания которые ты получил(а) тебе пригодятся в будущем и я выступил в роли катализатора и тебя теперь никто и ничто не остановит')
        await bot.send_message(message.from_user.id,
                               'Я буду ждать тебя сколько потребуется тут, если ты передумаешь нажми на кнопку ниже', reply_markup=keyboard)
        await state.set_state('wait_for_number')


@dp.message_handler(state='wait_for_number')
async def get_number(message: types.Message, state: FSMContext):
    # message.answer_contact() где-то нужно сохронять
    await bot.send_message(message.from_user.id,
                           'Славно, передал контакты нашим ребятам теперь хорошенько отдохни и ожидай звонка')
    await state.finish()


# получение профиля пользователя
async def get_profile(callback: CallbackQuery):
    data = db.get_full_info(callback.from_user.id)
    if data[1]:
        await bot.send_message(callback.from_user.id,
                               f"{data[0]}\n"
                               f"уровень: {data[1]}\n"
                               f"подписка: {'именется' if data[2] else 'не имеется'}\n"
                               f"монеты: {data[3]}\n"
                               f"дата подписки: {data[4]}\n"
                               f"дата окончания подписки: {data[5]}")
    else:
        await bot.send_message(callback.from_user.id, "Профиль доступен только регистрации.")
