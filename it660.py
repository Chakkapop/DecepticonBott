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
            print(parameters)
            if len(parameters) != 3:
                await message.channel.send("โปรดระบุเวลาให้ถูกต้อง (เช่น !set_timer 60)")
                return

            time_interval = parameters[1]
            name = parameters[2]
            strtime = ' '.join(time_interval)
            strtime = strtime.replace('/', '')
            if len(time_interval) <= 0:
                await message.channel.send("โปรดระบุเวลาให้มากกว่า 0")
                return

            user = message.author

            if user.id in timers:
                await message.channel.send("คุณมีตัวจับเวลาที่กำลังทำงานอยู่แล้ว")
            else:
                timers[user.id] = asyncio.create_task(
                    start_timer(user, time_interval, name))
                await message.channel.send("ตั้งเวลาสำเร็จ! จะแจ้งเตือนคุณก่อนกำหนดงาน 1 วัน")
        except ValueError:
            print(time_interval)
            await message.channel.send("โปรดระบุเวลาที่ถูกต้อง")


async def start_timer(user, time_interval, name):
    print(name)
    print(time_interval)
    now = datetime.now()
    formatted_date = now.strftime("%m-%d")
    formatted_date = str(formatted_date)
    date = formatted_date.replace('-', '')
    strtime = time_interval
    strtime = strtime.replace('/', '')
    print(date)
    print(strtime)
    use = user.mention
    text = use+name+' ถึงกำหนดแล้ว'+':skull:'
    text2 = use+name+' เหลือเวลาอีก 1 วัน' + ':calendar_spiral: '
    del timers[user.id]
    if int(date) + 1 == int(strtime):
        await user.guild.text_channels[4].send(text2)
    elif int(date) == int(strtime):
        await user.guild.text_channels[4].send(text)
client.run(
    'MTE1MTQzMjM2NTE4OTYzMjAwMg.G63r_E.kQtHdNl2w__1575gll9nrZRockLINfH76M9q4Q')
