import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(discord.Intents.default())
class MyClient(client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTE1MTQwNjE1NTY3MTgwNTk5NA.Gh8WBf.X1fHNVBxAefcQcff6Fmo8OJeRPZzGCVK6LFleg')