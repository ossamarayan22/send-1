import asyncio
from pyrogram import Client
from datetime import datetime, timedelta


api_id = '29275593'  
api_hash = '603ab55d3e4ef08eb95903cb1f72006d'  
phone_number = '+212611751954'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

message_text_hourly = "🎁 المكافأة اليوميه"
message_text_4_minutes = "مشاهدة الاعلانات 💸"

bot_username = '@USdularatbot'

MAX_MESSAGES_PER_DAY = 10
message_count = 0

def get_next_reset_time():
    now = datetime.now()
    reset_time = datetime.combine(now + timedelta(days=1), datetime.min.time())
    return reset_time

reset_time = get_next_reset_time()

async def send_message_every_4_minutes():
    global message_count, reset_time
    while True:
        if datetime.now() >= reset_time:
            message_count = 0
            reset_time = get_next_reset_time()  

        if message_count < MAX_MESSAGES_PER_DAY:
            await app.send_message(bot_username, message_text_4_minutes)
            message_count += 1
            print(f"4-minute message sent to {bot_username}, count: {message_count}/{MAX_MESSAGES_PER_DAY}")
        else:
            print("تم إرسال جميع الرسائل المسموح بها لهذا اليوم.")
        
        await asyncio.sleep(290)  


async def send_message_every_2_hours():
    while True:
        await asyncio.sleep(5)
        await app.send_message(bot_username, message_text_hourly)
        print(f"2-hour message sent to {bot_username}")
        await asyncio.sleep(7239)  

async def main():
    async with app:
        await asyncio.gather(
            send_message_every_4_minutes(),
            send_message_every_2_hours()
        )

if __name__ == "__main__":
    asyncio.run(main())