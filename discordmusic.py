import discord
import yt_dlp
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a song name with the command. For example: `!play [song name]`")

# Replace 'YOUR_TOKEN_HERE' with your bot token
bot.run('MTE1NjU1MTQ3NzUwNzEzMzQ3MA.G7pzCu.Z5l08U4A2SBRAgIZbrdKwNqB21U58CvfNPqTlo')
