import threading
from json import load

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ContentTypes
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from aiohttp import web

import functions as f
import scheduled as sc
from config import PAYMENTS_PROVIDER_TOKEN
from create_bot import dp, bot
from db import Database
from server import app

test = load(open("test.json", "r", encoding="utf-8"))
test_test = load(open("test_test.json", "r", encoding="utf-8"))
db = Database()
cb = CallbackData("kn", "question", "answer")
parse_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}


@dp.message_handler(commands='start')
async def hello(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        db.first_add(user_id)
        # a = await bot.send_animation(message.chat.id, animation=open('7Pp0.gif', 'rb'), caption="Загрузка видео...")
        #
        # video = YouTube('https://www.youtube.com/watch?v=ZQr7fzVp_KQ')
        # video_file_path = video.streams.get_highest_resolution().download()
        # clip = VideoFileClip(video_file_path)
        # width, height = clip.size
        # with open(video_file_path, 'rb') as video_file:
        #     await bot.send_video(chat_id=message.chat.id, video=video_file,
        #                          width=width, height=height,
        #                          caption='Privetstvennoe soopshenie')
        #     await bot.delete_message(message.chat.id, a.message_id)
        # os.remove(video_file_path)
        await bot.send_message(message.chat.id,
                               'Добро пожаловать в <b>Easy English</b> от <b>National Foundation Center!</b>\n'
                               'Мы рады приветствовать вас в нашем телеграм боте, где вы сможете получать увлекательные видеоуроки и интересные тесты для изучения английского языка. У нас есть всё, что вам нужно, чтобы улучшить свои навыки и достичь своих языковых целей.\n'
                               'Наши видеоуроки покрывают различные уровни сложности, от начинающих до продвинутых, а тесты помогут вам закрепить полученные знания.\n'
                               'Если вы хотите получить доступ к полному контенту и не упустить ни одного урока, рекомендуем приобрести подписку.\n'
                               'Так что давайте начнем увлекательное путешествие в мир английского языка вместе! Если у вас есть какие-либо вопросы, не стесняйтесь обращаться к нам.\n'
                               'Удачи в изучении английского языка, и до скорой встречи на наших уроках! 🚀🌟\n')

        await bot.send_message(message.chat.id, 'Прошу напишите мне своё имя и фамилию.\n'
                                                '<b>(Любое написанное вами далее сообщение будет записана в качестве вашего ФИО и будет использовано лишь для обращения к вам. Его всегда можно будет поменять.)</b>')
        await state.set_state('wait_for_name')
    else:
        await bot.send_message(message.chat.id, "Вы уже в базе.")


@dp.message_handler(state='wait_for_name')
async def process_name(message: types.Message, state: FSMContext):
    fio = message.text
    db.set_fio(message.from_user.id, fio)
    await state.finish()
    await state.update_data(username=fio)
    await bot.send_message(message.chat.id, f"Так и запишем, {fio}!\n"
                                            "Чтобы проверить свой уровень знаний введи команду /test\n"
                                            "<b>У тебя есть только одна попытка</b>")


def compose_markup(number: int):
    question = "test_" + str(number)
    kn = InlineKeyboardMarkup(row_width=1)

    cdA = {
        "question": number,
        "answer": "A"
    }
    kn.insert(InlineKeyboardButton(test_test[question]["A"], callback_data=cb.new(number, "A")))
    cdB = {
        "question": number,
        "answer": "B"
    }
    kn.insert(InlineKeyboardButton(test_test[question]["B"], callback_data=cb.new(number, "B")))
    cdC = {
        "question": number,
        "answer": "C"
    }
    kn.insert(InlineKeyboardButton(test_test[question]["C"], callback_data=cb.new(number, "C")))
    return kn


@dp.callback_query_handler(cb.filter())
@dp.throttled(rate=2)
async def answer_handler(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    data = callback_data
    q = "test_" + str(data["question"])
    is_correct = test_test[q]["Correct"] == data["answer"]
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
        db.upd_msg(user_id, 0)
        db.upd_passed(user_id, 0)
        db.upd_process(user_id, False)
        intro = {"Beginner": "https://youtu.be/_ffiSFzHLw4",
                 "Elementary": "https://youtu.be/CT6a4jKfuzs",
                 "Pre-Intermediate": "https://youtu.be/oTqX1r3SFHI",
                 "Intermediate": "https://youtu.be/aQbXt2f4Pag",
                 "Upper-Intermediate": "https://youtu.be/HYyx3_X7zrE"}
        await bot.send_message(callback.from_user.id,
                               f"Конец. Лови вступительный видеоурок по твоему уровню: {intro[db.get_level(user_id)[0]]}\n"
                               f"Ваш уровень английского: <b>{db.get_level(user_id)[0]}</b> \n"
                               f"Вы набрали <b>{score}</b> баллов из 25")
        await bot.send_invoice(callback.from_user.id, title='подписка на 1 месяц ',
                               description=f"Поздравляем с прохождением пробного экзамена.Но это еще не все. Оформив платную подписку вы получаете: \n"
                                           f"Доступ более чем 150 видео для обучения английскому языку. \n"
                                           f"Тесты для закрепления матерьяла. \n"
                                           f"И много всего другово.",
                               currency='kzt',
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               prices=[types.LabeledPrice(label='Подписка на один месяц', amount=7000)]
                               )

        return
    q = "test_" + str(int(data["question"]) + 1)
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                text=test_test[q]["question_1"],
                                message_id=msg,
                                reply_markup=compose_markup(int(data["question"]) + 1))


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'поздравляяем с покупкой')
    await db.give_subscription(message.chat.id, 1)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Во время оплаты произошла ошибка. Попробуйте позже ")


@dp.message_handler(commands='testSTOP')
async def check_level(message: types.Message):
    user_id = message.from_user.id
    if db.get_level(user_id)[0]:
        await bot.send_message(message.from_user.id, "Вы уже сдавали проверочный экзамен ")
        return
    if db.get_process(user_id)[0]:
        await bot.send_message(message.from_user.id, "Тест уже идёт")
        return
    db.upd_process(user_id, True)
    db.upd_passed(user_id, 0)
    msg = await bot.send_message(
        message.from_user.id,
        test_test["test_1"]["question_1"],
        reply_markup=compose_markup(1)
    )
    db.upd_msg(user_id, msg.message_id)


@dp.message_handler(commands='test')
async def check_level(message: types.Message):
    user_id = message.from_user.id
    if db.get_level(user_id)[0]:
        await bot.send_message(user_id, "Вы уже сдавали проверочный экзамен ")
        return
    if db.get_process(user_id)[0]:
        await bot.send_message(user_id, "Тест уже идёт")
        return
    db.upd_process(user_id, True)
    db.upd_passed(user_id, 0)
    await f.compose_poll(user_id)


@dp.poll_answer_handler()
async def poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    db.upd_question(user_id, db.get_question(user_id)[0] + 1)
    if db.get_options(user_id)[0] == poll_answer.option_ids[0]:
        passed = db.get_passed(user_id)[0] + 1
        db.upd_passed(user_id, passed)
    await bot.delete_message(user_id, db.get_msg(user_id)[0])
    await f.compose_poll(user_id)


@dp.message_handler(commands=['profile'])
async def id_from_message(message: types.message_id):
    await f.get_profile(message)


@dp.message_handler(commands=['feedBack'])
async def id_from_message(message: types.message_id):
    await f.send_feedback(message)


def server():
    web.run_app(app, port=8060)


if __name__ == '__main__':
    threading.Thread(target=server).start()
    executor.start_polling(dp, skip_updates=True, on_startup=sc.on_startup)
