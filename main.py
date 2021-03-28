import discord
import os
import cowsay

client = discord.Client()

@client.event
async def on_ready():
    print('cowsay ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!cowsay'):
        content = message.content[len('!cowsay '):]
        await message.channel.send('```\n' + cowsay.cow(content) + '\n```')

client.run(os.getenv('TOKEN'))
