from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram import types
from aiogram.utils.callback_data import CallbackData

import scheduled as sc
import functions as f
from create_bot import dp, bot
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from db import Database

from json import dumps, loads, load

import aioschedule

test = load(open("test.json", "r", encoding="utf-8"))
test_test = load(open("test_test.json", "r", encoding="utf-8"))
db = Database()
cb = CallbackData("kn", "question", "answer")

@dp.message_handler(commands=['start'])
async def hello(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not db.user_exists(user_id):
        db.first_add(user_id)
        a = await bot.send_animation(message.chat.id, animation=open('7Pp0.gif', 'rb'), caption="Загрузка видео...")

        video = YouTube('https://www.youtube.com/watch?v=ZQr7fzVp_KQ')
        video_file_path = video.streams.get_highest_resolution().download()
        clip = VideoFileClip(video_file_path)
        width, height = clip.size
        with open(video_file_path, 'rb') as video_file:
            await bot.send_video(chat_id=message.chat.id, video=video_file,
                                 width=width, height=height,
                                 caption='Privetstvennoe soopshenie')
            await bot.delete_message(message.chat.id, a.message_id)
        os.remove(video_file_path)

        await bot.send_message(message.chat.id, 'А как мне тебя звать?')
        await state.set_state('wait_for_name')


@dp.message_handler(state='wait_for_name')
async def process_name(message: types.Message, state: FSMContext):
    fio = message.text
    db.set_fio(message.from_user.id, fio)
    await state.finish()
    await state.update_data(username=fio)
    await bot.send_message(message.chat.id, f"Так и запишем, {fio}!\n"
                                            f"Если ты уже произвел оплату просто введи команду\n"
                                            f"/subscription чтобы начать обучение")


@dp.message_handler(commands=['subscription'])
async def check_sub(message: types.Message):
    user_id = message.from_user.id
    if db.check_sub(user_id)[0]:
        await bot.send_message(message.chat.id,
                               "Регистрация прошла успешно. Добро пожаловать в мир английского языка вместе с NFC\n"
                               "Чтобы проверить свой уровень знаний напиши мне 'TEST'")
    else:
        await bot.send_message(message.chat.id, "Ошибка регистрации")


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
        await bot.send_message(callback.from_user.id, f"END.\n"
                                                      f"Ваш уровень английского:*{db.get_level(user_id)[0]}*\\n"
                                                      f"Вы набрали *{score}*\ баллов из 25", parse_mode="MarkdownV2")
        return
    q = "test_" + str(int(data["question"]) + 1)
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                text=test_test[q]["question_1"],
                                message_id=msg,
                                reply_markup=compose_markup(int(data["question"]) + 1))


@dp.message_handler(text='TEST')
async def check_level(message: types.Message):
    user_id = message.from_user.id
    if db.get_level(user_id)[0]:
        await bot.send_message(message.from_user.id, "Вы уже сдавали проверочный экзамен ")
        return
    if db.get_process(user_id)[0]:
        await bot.send_message(message.from_user.id,
                               "Тест уже идёт")
        return
    db.upd_process(user_id, True)
    db.upd_passed(user_id, 0)
    msg = await bot.send_message(
        message.from_user.id,
        test_test["test_1"]["question_1"],
        reply_markup=compose_markup(1)
    )
    db.upd_msg(user_id, msg.message_id)


@dp.message_handler(commands=['profile'])
async def id_from_message(message: types.message_id):
    await f.get_profile(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=sc.on_startup)
