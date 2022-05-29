#!/usr/bin/env python3

from os import getenv

import cowsay
import discord
import discord_slash

client = discord.ext.commands.Bot(intents=discord.Intents(), command_prefix="!")
slash = discord_slash.SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    cowsay.cow("I'm ready!")

options = options=[
    discord_slash.utils.manage_commands.create_option(
        name="character", description="Choose your character!" , option_type=3, required=True, choices = [
            discord_slash.utils.manage_commands.create_choice(name=character, value=character) for character in cowsay.char_names
        ]
    ),
    discord_slash.utils.manage_commands.create_option(
        name="message", description="What do you want to say?" , option_type=3, required=True
    )
]

guild_ids = [int(guild_id) for guild_id in getenv('GUILD_IDS').split(" ")]

@slash.slash(name="cowsay", guild_ids=guild_ids, options=options)
async def cowsayfunc(ctx, character: str, message: str):
    await ctx.send(content=f'```\n{cowsay.get_output_string(character, message)}```\n')

client.run(getenv('TOKEN'))
