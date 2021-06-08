import discord
import cowsay

import os
import re
import random

client = discord.Client()

@client.event
async def on_ready():
    print('cowsay ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        if match := re.search('^!([^ ]+)say (.*)', message.content):
            animal = match[1].lower()
            response = match[2]

            if animal not in cowsay.char_names:
                response = f'You wanted "{animal}" but only the following animals exist: {", ".join(cowsay.char_names)}'
                animal = random.choice(list(cowsay.char_names))

            await message.channel.send(f'```\n{cowsay.get_output_string(animal, response)}\n```')
    except Exception as e:
        await message.channel.send(f'{message.author} said {message.content}, but:\n{e}')

client.run(os.getenv('TOKEN'))
