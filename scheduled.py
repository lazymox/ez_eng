from json import load
import schedule
import aioschedule
from db import Database
import asyncio
import pytz
from datetime import datetime, date
import functions as f
import time
import threading

from server import app

db = Database()
test = load(open("test.json", "r", encoding="utf-8"))
video = load(open("video.json", "r", encoding="utf-8"))


async def daily():
    uids = db.get_user_ids()
    for user_id in uids:
        level = db.get_level(user_id)[0]
        progress = db.get_leveling(user_id)[0]
        video_link = video[level][str(progress)]["video_1"]
        video_test = video[level][str(progress)]["test"]
        await f.video_send(video_link, user_id)
        if video_test != "0":
            await f.prep_test_mess(user_id)
        else:
            progress += 1
            db.upd_leveling(user_id, progress)


# функция  для обнуления статуса подписки
async def subscription_scheduler():
    dates = await db.get_subscritions_time()
    current_date = datetime.now().strftime('%Y-%m-%d')
    for end_day in dates:
        if end_day[0] == current_date:
            db.remove_subscrition(end_day[1])
            await f.end_subscription_notifier(end_day[1])


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every().day.at('00:00').do(run_threaded, subscription_scheduler)  # планировщик для статуса подписок


async def scheduler():
    kazakhstan_tz = pytz.timezone('Asia/Almaty')
    while True:
        schedule.run_pending()
        now = datetime.now(tz=kazakhstan_tz)
        if now.hour == 14 and now.minute == 6:
            await daily()
        await asyncio.sleep(60)


async def on_startup(_):
    asyncio.create_task(scheduler())
