import asyncio
from pyrogram import Client
from datetime import datetime, timedelta, time
from datetime import datetime, timedelta, timezone


api_id = '29275593'  
api_hash = '603ab55d3e4ef08eb95903cb1f72006d'  
phone_number = '+212611751954'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

message_text_hourly = "🎁 المكافأة اليوميه"
message_text_4_minutes = "مشاهدة الأعلانات💸"

bot_username = '@USdularatbot'

MAX_MESSAGES_PER_DAY = 10
message_count = 0

# حساب التوقيت المغربي بناءً على التوقيت المحلي (من غير `pytz`)
def get_morocco_time():
    utc_now = datetime.now(timezone.utc)  # استخدام timezone.utc للحصول على التوقيت UTC
    # في المغرب الشتوي (UTC+1)، وفي الصيف (UTC+0)
    # التوقيت الصيفي في المغرب يبدأ من آخر يوم أحد في مارس وينتهي آخر يوم أحد في أكتوبر
    if utc_now.month > 3 and utc_now.month < 10:  # من أبريل إلى أكتوبر
        return utc_now + timedelta(hours=1)  # التوقيت الصيفي (UTC+1)
    else:
        return utc_now  # التوقيت الشتوي (UTC+0)

async def send_message_10_times():
    global message_count
    count = 0
    while count < MAX_MESSAGES_PER_DAY:
        await app.send_message(bot_username, message_text_4_minutes)
        count += 1
        print(f"تم إرسال الرسالة {count}/{MAX_MESSAGES_PER_DAY}")
        await asyncio.sleep(240)  # الانتظار 4 دقائق بين كل رسالة وأخرى

async def send_message_every_2_hours():
    while True:
        await asyncio.sleep(5)  # الانتظار لمدة 5 ثواني قبل إرسال أول رسالة
        await app.send_message(bot_username, message_text_hourly)
        print(f"تم إرسال رسالة المكافأة اليومية إلى {bot_username}")
        await asyncio.sleep(7200)  # الانتظار ساعتين بين كل رسالة

async def main():
    async with app:
        # بداية إرسال الرسائل كل ساعتين بشكل مستقل
        asyncio.create_task(send_message_every_2_hours())
        
        while True:
            current_time = get_morocco_time().time()

            # إذا كان الوقت بين 1:00 ليلاً و 2:00 صباحاً
            if time(1, 0) <= current_time < time(2, 0):
                print("بدء الإرسال من 1:00 ليلاً إلى 2:00 صباحاً")
                await send_message_10_times()
                print("انتهى الإرسال للفترة الأولى")

            # إذا كان الوقت بين 10:00 ليلاً و 11:00 ليلاً
            elif time(22, 0) <= current_time < time(23, 0):
                print("بدء الإرسال من 10:00 ليلاً إلى 11:00 ليلاً")
                await send_message_10_times()
                print("انتهى الإرسال للفترة الثانية")

            # الانتظار لمدة دقيقة قبل التحقق مرة أخرى
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())