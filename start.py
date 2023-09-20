import discord


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.content == '555':
        await message.channel.send('ขำมากมั้ง')
    elif message.content == 'ถถถ':
        await message.channel.send('ขำมากมั้ง')
    elif message.content == '!welcome':
        await message.channel.send('Hello' + " " + str(message.author))
client.run("Token here")