import discord
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

timers = {}  # ใช้เก็บตัวจับเวลาแต่ละผู้ใช้


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!set_timer'):
        try:
            parameters = message.content.split(' ')
            if len(parameters) != 2:
                await message.channel.send("โปรดระบุเวลาให้ถูกต้อง (เช่น !set_timer 60)")
                return

            time_interval = parameters[1:]
            strtime = ' '.join(time_interval)
            strtime = strtime.replace('/', '')
            print(strtime)
            if len(time_interval) <= 0:
                await message.channel.send("โปรดระบุเวลาให้มากกว่า 0")
                return

            user = message.author
            print(user.id)
            print(timers)

            if user.id in timers:
                await message.channel.send("คุณมีตัวจับเวลาที่กำลังทำงานอยู่แล้ว")
                print(timers)
            else:
                timers[user.id] = asyncio.create_task(
                    start_timer(user, time_interval))
                await message.channel.send("ตั้งเวลาสำเร็จ! จะแจ้งเตือนคุณก่อนกำหนดงาน 1 วัน")
                print(timers)
        except ValueError:
            print(time_interval)
            await message.channel.send("โปรดระบุเวลาที่ถูกต้อง")


async def start_timer(user, time_interval):
    now = datetime.now()

    # แสดงเฉพาะวัน
    formatted_date = now.strftime("%m-%d")
    formatted_date = str(formatted_date)
    date = formatted_date.replace('-', '')
    print(date)
    strtime = ' '.join(time_interval)
    strtime = strtime.replace('/', '')
    del timers[user.id]
    if int(date) + 1 == int(strtime):
        await user.guild.text_channels[4].send(f"{user.mention}, ถึงเวลาที่คุณตั้งไว้แล้ว!")
    elif int(date) == int(strtime):
        await user.guild.text_channels[4].send(f"{user.mention}, งานถึงกำหนดแล้ว:skull: ")
client.run(
    'MTE1MTQzMjM2NTE4OTYzMjAwMg.GVpzrd.GuJ1Ib8Po6UkM2FmMueWn9bxQXgUMRYs5saz14')
