import threading
from json import load
from multiprocessing import Process

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from aiohttp import web

import functions as f
import scheduled as sc
from create_bot import dp, bot
from db import Database
from server import app

test = load(open("test.json", "r", encoding="utf-8"))
test_test = load(open("test_test.json", "r", encoding="utf-8"))
db = Database()
cb = CallbackData("kn", "question", "answer")


@dp.message_handler(commands='start')
async def hello(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        db.first_add(user_id)

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
        await bot.send_message(message.chat.id, "Ты уже в базе.")


@dp.message_handler(state='wait_for_name')
async def process_name(message: types.Message, state: FSMContext):
    fio = message.text
    db.set_fio(message.from_user.id, fio)
    await state.finish()
    await state.update_data(username=fio)
    await bot.send_message(message.chat.id, f"Так и запишем, {fio}!\n"
                                            "Чтобы проверить свой уровень знаний введи команду /test\n"
                                            "<b>У тебя есть только одна попытка</b>")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'поздравляяем с покупкой')
    db.give_subscription(message.chat.id, 1)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Во время оплаты произошла ошибка. Попробуйте позже ")


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


@dp.callback_query_handler(text="start_test")
async def start_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    if db.get_process(user_id)[0]:
        await bot.send_message(user_id, "Тест уже идёт")
        return
    db.upd_process(user_id, True)
    db.upd_passed(user_id, 0)
    db.upd_question(user_id, 1)
    await bot.delete_message(user_id, db.get_msg(user_id)[0])
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


@dp.message_handler(commands=['subscription'])
async def id_from_message(message: types.message_id):
    if db.check_sub(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               f'У вас уже есть подписка. Мы уведомим вас о надобности покупки подписки. ')
    else:
        payload = 'sub' if db.check_sub(message.from_user.id)[0] is None else 'resub'
        await f.invoice(message.from_user.id, 'подписка', 'описание', payload)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    match message.successful_payment.invoice_payload:
        case 'sub':
            await bot.send_message(message.chat.id,
                                   'Поздравляяем с покупкой.Короче раскад такой.Каждый день в 15.00 тебе будет приходить тест вместе с раздаточным матерьялом.Проходя тест ты продвигаешся дальше')
        case 'resub':
            await bot.send_message(message.chat.id, 'поздравляяем с покупкой')
    db.give_subscription(message.chat.id, 1)
    name = db.get_fio(message.chat.id)[0]
    db.insert_payments([message.chat.id, name])


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Во время оплаты произошла ошибка. Попробуйте позже ")


def server():
    web.run_app(app, port=8060)
    return app


if __name__ == '__main__':
    Process(target=server).start()
    executor.start_polling(dp, skip_updates=True, on_startup=sc.on_startup)

