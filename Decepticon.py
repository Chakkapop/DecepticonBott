import discord
import yt_dlp
from discord.ext import commands
from datetime import datetime
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
timers = {}  # ใช้เก็บตัวจับเวลาแต่ละผู้ใช้
@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def play(ctx, *, song):
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'ytsearch:{song}', download=False)
        url = info['entries'][0]['url']

    vc.stop()
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url))

@bot.command()
async def skip(ctx):
    if not ctx.voice_client:
        await ctx.send("The bot is not in a voice channel.")
        return

    ctx.voice_client.stop()
    await ctx.send("The current song has been skipped.")


@bot.command()
async def disconnect(ctx):
    if not ctx.voice_client:
        await ctx.send("The bot is not in a voice channel.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    await ctx.voice_client.disconnect()
    await ctx.send("The bot has been disconnected from the voice channel.")

def get_counterpicknet_counterpicks(champion):#league of legends  Ex:!counterpick champion opgg
    return f"https://www.counterstats.net/league-of-legends/{champion}"
def get_opgg_counterpicks(champion):
    return f"https://www.op.gg/champions/{champion}/counters"

@bot.command(name="counterpick", aliases=["cp"])
async def counterpick(ctx, champion: str, website: str = "opgg"):

    if not champion:
        await ctx.channel.send("Please specify a champion name.")
        return

    if website.lower() not in ["opgg", "counterstats"]:
        await ctx.channel.send("Please choose either 'opgg' or 'counterstats' as the website.")
        return

    if website.lower() == "opgg":
        counterpicks_link = get_opgg_counterpicks(champion)
    else:
        counterpicks_link = get_counterpicknet_counterpicks(champion)

    await ctx.send(f"Counterpicks for {champion} on {website}: {counterpicks_link}")

#main code
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if message.content.startswith('!set_work'):
        try:
            parameters = message.content.split(' ')
            print(parameters)
            if len(parameters) != 3:
                await message.channel.send("โปรดระบุเวลาให้ถูกต้อง (เดือน/วัน ชื่องาน)")
                return

            time_interval = parameters[1]
            name = parameters[2]
            strtime = ' '.join(time_interval)
            strtime = strtime.replace('/', '')
            if len(time_interval) <= 0:
                await message.channel.send("โปรดระบุเวลาให้ถูกต้อง (เดือน/วัน ชื่องาน)")
                return

            user = message.author

            timers[user.id] = asyncio.create_task(
                start_timer(user, time_interval, name))
            await message.channel.send("ตั้งเวลาสำเร็จ! จะแจ้งเตือนคุณก่อนกำหนดงาน 1 วัน")
        except ValueError:
            print(time_interval)
            await message.channel.send("โปรดระบุเวลาให้ถูกต้อง (เดือน/วัน ชื่องาน)")


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
        await user.guild.text_channels[1].send(text2)
    if int(date) == int(strtime):
        await user.guild.text_channels[1].send(text)

# Replace 'Token' with your bot token
bot.run('Token')