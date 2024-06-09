#!/usr/bin/env python3

import datetime

from dotenv import dotenv_values
from os import getenv

import cowsay

import discord

dotenv = dotenv_values(".env")

TOKEN = getenv("TOKEN") or dotenv["TOKEN"]
if not TOKEN:
    raise Exception("TOKEN environment variable must be defined")

GUILD_IDS = getenv("GUILD_IDS") or dotenv["GUILD_IDS"]
if not GUILD_IDS:
    raise Exception("GUILD_IDS environment variable must be defined")
GUILD_IDS = [int(guild_id) for guild_id in GUILD_IDS.split(",")]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

GUILDS = [discord.Object(guild_id) for guild_id in GUILD_IDS]

@tree.command(
    name="cowsay",
    description="cowsay for GNU/Linux was initially written in perl by Tony Monroe",
    guilds=GUILDS,
)
async def _cowsay(
        interaction: discord.Interaction,
        character: str,
        text: str,
):
    print(f"Sending a {character} at {datetime.datetime.now()}")
    await interaction.response.send_message(f'```\n{cowsay.get_output_string(character.lower(), text)}\n```')

@_cowsay.autocomplete("character")
async def character_autocomplete(
        interaction: discord.Interaction,
        current: str,
):
    return [
        discord.app_commands.Choice(name=char, value=char)
        for char in cowsay.char_names if current.lower() in char
    ][:25]
    

@client.event
async def on_ready():
    for guild in GUILDS:
        await tree.sync(guild=guild)
    cowsay.cow(f"I'm ready! GUILD_IDS={GUILD_IDS}")

client.run(TOKEN)
