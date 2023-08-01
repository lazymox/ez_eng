from json import load

from db import Database
import asyncio
import pytz
from datetime import datetime, date
import functions as f

db = Database()
test = load(open("test.json", "r", encoding="utf-8"))
video = load(open("video.json", "r", encoding="utf-8"))


async def daily():
    uids = db.get_user_ids()
    for user_id in uids:
        if db.get_try(user_id)[0] != 0:
            continue
        level = db.get_level(user_id)[0]
        progress = db.get_leveling(user_id)[0]
        video_link = video[level][str(progress)]["video_1"]
        video_test = video[level][str(progress)]["test"]
        await f.video_send(video_link, user_id)
        await f.razdatka(user_id)
        if video_test != "0":
            await f.prep_test_mess(user_id)
        else:
            progress += 1
            db.upd_leveling(user_id, progress)


# функция  для обнуления статуса подписки
async def subscription_scheduler():
    dates = db.get_subscritions_time()
    current_date = datetime.now().strftime('%Y-%m-%d')
    for end_day in dates:
        if end_day[1].strftime('%Y-%m-%d') == current_date:
            db.remove_subscription(end_day[0])
            await f.end_subscription_notifier(end_day[0])


async def scheduler():
    kazakhstan_tz = pytz.timezone('Asia/Almaty')
    while True:
        now = datetime.now(tz=kazakhstan_tz)
        # if now.hour == 24:
        #     await daily()
        # if now.hour == 15:
        #     await subscription_scheduler()
        # await asyncio.sleep(60)
        await daily()
        await asyncio.sleep(300)


async def on_startup(_):
    asyncio.create_task(scheduler())
