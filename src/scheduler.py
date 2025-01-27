# filepath: /c:/Users/Abnet/Desktop/telethon_bot/telethon_bot/src/scheduler.py
import asyncio
import datetime
from broadcast import send_broadcast
 
def schedule_message(client, message, schedule_time):
    delay = (schedule_time - datetime.datetime.now()).total_seconds()
    asyncio.get_event_loop().call_later(delay, asyncio.create_task, send_broadcast(client, message))