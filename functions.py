import asyncio
import os
from json import load

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from config import PAYMENTS_PROVIDER_TOKEN
from create_bot import dp, bot
from db import Database

db = Database()
test = load(open("test.json", "r", encoding="utf-8"))
test_test = load(open("test_test.json", "r", encoding="utf-8"))
video = load(open("video.json", "r", encoding="utf-8"))
cd = CallbackData("km", "question", "answer")
parse_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}

promote_text = "Перед тем как я с тобой попрощаюсь навсегда хочу тебе предложить 1 вещь который возможно тебя заинтересует называется он NCF English и там ты сможешь быть самым лучшим в группе ведь у тебя есть преимущества в виде меня и от меня символический подарок, скидка поскольку я уважаю твой труд и время"

intro = {"Beginner": "https://youtu.be/_ffiSFzHLw4",
         "Elementary": "https://youtu.be/CT6a4jKfuzs",
         "Pre-Intermediate": "https://youtu.be/oTqX1r3SFHI",
         "Intermediate": "https://youtu.be/aQbXt2f4Pag",
         "Upper-Intermediate": "https://youtu.be/HYyx3_X7zrE"}


# отправка видео
async def video_send(link, user_id):
    await bot.send_message(user_id, link)


# хочешь начать тест?
async def prep_test_mess(user_id):
    knopka = InlineKeyboardMarkup()
    knopka.insert(InlineKeyboardButton("жми", callback_data="start_test"))
    msg = await bot.send_message(user_id, "Когда будешь готов начать тест, нажми на кнопку ниже", reply_markup=knopka)
    db.upd_msg(user_id, msg.message_id)


# сообщение о конце обучения
async def end_mess(user_id):
    kb = [[types.InlineKeyboardButton(text="Да", callback_data='answer_yes')],
          [types.InlineKeyboardButton(text="Нет", callback_data='answer_no')]]
    keyboard = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=kb)
    coin = db.get_coin(user_id)[0]
    await bot.send_message(user_id, f'Поздравляю это конец, ты набрал вот столько коинов: {coin}\n'
                                    f'Вот такие то у тебя скидки короче похуй')
    await bot.send_message(user_id, promote_text, reply_markup=keyboard)


@dp.callback_query_handler(text='answer_yes')
async def answer_yes(call: types.callback_query, state: FSMContext):
    await bot.edit_message_text(text=promote_text, chat_id=call.from_user.id, message_id=call.message.message_id,
                                reply_markup=None)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отправить контакт", request_contact=True))
    await bot.send_message(call.from_user.id,
                           "Рад видеть что у тебя есть рвение изучать язык дальше, напиши мне свои контактные данные (ФИО и номер телефона) я передам нашим специалистам они обязательно с тобой свяжутся",
                           reply_markup=keyboard)
    await state.set_state('wait_number')


@dp.callback_query_handler(text='answer_no')
async def answer_no(call: types.callback_query, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text="отправить контакт", request_contact=True))
    await bot.send_message(call.from_user.id,
                           'На нет и суда нет, это только твоё право, уверен что знания которые ты получил(а) тебе пригодятся в будущем и я выступил в роли катализатора и тебя теперь никто и ничто не остановит')
    await bot.send_message(call.from_user.id,
                           'Я буду ждать тебя сколько потребуется тут, если ты передумаешь нажми на кнопку ниже',
                           reply_markup=keyboard)
    await state.set_state('wait_number')


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state='wait_number')
async def get_contact(message, state: FSMContext):
    name = db.get_fio(message.from_user.id)[0]
    db.insert_completed(
        [message.from_user.id, name, message.contact.phone_number])
    await bot.send_message(message.from_user.id,
                           'Славно, передал контакты нашим ребятам теперь хорошенько отдохни и ожидай звонка',
                           reply_markup=types.ReplyKeyboardRemove())

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


async def send_feedback(message):
    data = db.get_full_info(message.from_user.id)
    if data[1]:
        if message.get_args() == '':
            await bot.send_message(message.from_user.id,
                                   'Чтобы отправить обращение разработчику, напишите /feedback и подробный текст обращения, например <pre>/feedback Прошу добавить возможность ...</pre> ',
                                   parse_mode='HTML')
        else:
            await bot.send_message(message.from_user.id, 'Сообщение отправлено. Мы расмотрим ваше обращение')
            db.insert_feedback([message.from_user.id, message.get_args()])
    else:
        await bot.send_message(message.from_user.id, "функция доступна только после регистрации.")


async def end_subscription_notifier(user_id):
    await invoice(user_id, 'Переоформление подписки',
                  'Ваша подписка истекла.Пока вы ее не переоформите вам не будут приходить новые '
                  'материалы ', 'resub')


async def razdatka(user_id):
    urok = 'Урок ' + str(db.get_leveling(user_id)[0])
    folder_path = f'Раздатки/{db.get_level(user_id)[0]}/{urok}'
    try:
        for file_name in os.listdir(folder_path):
            pdf_path = os.path.join(folder_path, file_name)
            with open(pdf_path, 'rb') as pdf_file:
                await bot.send_document(user_id, pdf_file)
    except:
        pass


async def compose_poll(user_id):
    if not db.get_level(user_id)[0]:
        q = "test_" + str(db.get_question(user_id)[0])

        if q == "test_26":
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

            db.upd_msg(user_id, 0)
            db.upd_passed(user_id, 0)
            db.upd_process(user_id, False)
            await bot.send_message(user_id,
                                   f"Конец. Лови вступительный видеоурок по твоему уровню: {intro[db.get_level(user_id)[0]]}\n"
                                   f"Ваш уровень английского: <b>{db.get_level(user_id)[0]}</b> \n"
                                   f"Вы набрали <b>{score}</b> баллов из 25")
            await invoice(user_id, 'подписка на 1 месяц ',
                          f"Поздравляем с прохождением пробного экзамена.Но это еще не все. Оформив платную подписку вы получаете: \n"
                          f"Доступ более чем 150 видео для обучения английскому языку. \n"
                          f"Тесты для закрепления матерьяла. \n"
                          f"И много всего другово.",
                          'sub'
                          )
            return
        question = f"[{db.get_question(user_id)[0]}/25] " + test_test[q]["question_1"]
        options = []
        options.append(test_test[q]["A"])
        options.append(test_test[q]["B"])
        options.append(test_test[q]["C"])

        correct_option_id = parse_to_index[test_test[q]["Correct"]]
        db.upd_options(user_id, parse_to_index[test_test[q]["Correct"]])

        msg = await bot.send_poll(
            user_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_option_id
        )
        db.upd_msg(user_id, msg.message_id)
    else:
        level = db.get_level(user_id)[0]
        progress = db.get_leveling(user_id)[0]
        num = video[level][str(progress)]["test"]
        last = False
        if num == "final":
            last = True
        testNum = "test_" + num
        testing = test[level][testNum]

        q = db.get_question(user_id)[0]

        if str(q) not in testing.keys():
            q = int(q) - 1
            score = db.get_passed(user_id)[0]
            if score >= int(q) * 0.7:
                tries = db.get_try(user_id)[0]
                if tries == 0:
                    db.upd_coin(user_id, db.get_coin(user_id)[0] + 3)
                elif tries == 1:
                    db.upd_coin(user_id, db.get_coin(user_id)[0] + 2)
                else:
                    db.upd_coin(user_id, db.get_coin(user_id)[0] + 1)
                db.upd_try(user_id, 0)
                await bot.send_message(user_id,
                                       f"Поздравляю <b>{db.get_fio(user_id)[0]}</b>, ты набрал <b>{score}</b> из <b>{q}</b>")
                db.upd_try(user_id, 0)
                db.upd_process(user_id, 0)
                if last:
                    if level == "Beginner":
                        db.upd_level(user_id, "Elementary")
                    if level == "Elementary":
                        db.upd_level(user_id, "Pre-Intermediate")
                    if level == "Pre-Intermediate":
                        db.upd_level(user_id, "Intermediate")
                    if level == "Intermediate":
                        db.upd_level(user_id, "Upper-Intermediate")
                    if level == "Upper-Intermediate":
                        db.upd_level(user_id, "COMPLETED")
                        db.remove_subscription(user_id)
                        await end_mess(user_id)
                        return
                    await bot.send_message(user_id, f"Какой же ты молодец!\n"
                                                    f"Теперь можешь хвастатся друзьям своим новым уровнем английского: <b>{db.get_level(user_id)[0]}</b>\n"
                                                    f"Лови вступительный видеоурок по твоему новому уровню: {intro[db.get_level(user_id)[0]]}")
                    db.upd_leveling(user_id, 1)
                    return
                db.upd_leveling(user_id, db.get_leveling(user_id)[0] + 1)
            else:
                await bot.send_message(user_id, f"Ой! <b>{db.get_fio(user_id)[0]}</b>, похоже ты не сдал.\n"
                                                f"Ты набрал <b>{score}</b> из <b>{q}</b>.\n"
                                                f"Повтори прошедшие задания и попробуй снова через 2 часа, иначе дальше не пройдешь!")
                db.upd_try(user_id, db.get_try(user_id)[0] + 1)
                db.upd_question(user_id, 1)
                db.upd_process(user_id, 0)
                db.upd_passed(user_id, 0)
                await asyncio.sleep(60)
                await prep_test_mess(user_id)
            return

        q = str(q)
        if "11" in testing.keys():
            question = f"[{q}/20] " + testing[q]["question"]
        else:
            question = f"[{q}/10] " + testing[q]["question"]
        options = []
        options.append(testing[q]["A"])
        options.append(testing[q]["B"])
        if "C" in testing[q].keys():
            options.append(testing[q]["C"])

        if "D" in testing[q].keys():
            options.append(testing[q]["D"])

        correct_option_id = parse_to_index[testing[q]["Correct"]]
        db.upd_options(user_id, parse_to_index[testing[q]["Correct"]])

        msg = await bot.send_poll(
            user_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_option_id
        )
        db.upd_msg(user_id, msg.message_id)


async def invoice(user_id, title, description, payload):
    await bot.send_invoice(user_id, title=title,
                           description=description,
                           currency='KZT',
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           payload=payload,
                           prices=[types.LabeledPrice(label='Подписка на один месяц', amount=7000 * 100)],
                           need_name=False,
                           need_shipping_address=False,
                           protect_content=True,
                           need_email=False,
                           need_phone_number=False,
                           start_parameter='subscription'
                           )
