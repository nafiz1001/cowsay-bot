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
GUILDS = [discord.Object(guild_id) for guild_id in GUILD_IDS]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(
    name="cowsay",
    description="Make a character say something.",
    guilds=GUILDS,
)
async def _cowsay(
        interaction: discord.Interaction,
        character: str,
        text: str,
):
    print(f"Sending a {character} at {datetime.datetime.now()}")
    character = character.lower()
    if character in cowsay.CHARS:
        await interaction.response.send_message(f"```\n{cowsay.get_output_string(character, text)}\n```")
    else:
        say = cowsay.get_output_string("cow", f"{character} does not exist as a character. Try the following: {', '.join(cowsay.char_names)}.")
        await interaction.response.send_message(f"```\n{say}\n```")

@_cowsay.autocomplete("character")
async def character_autocomplete(
        interaction: discord.Interaction,
        current: str,
):
    current = current.lower()
    return [
        discord.app_commands.Choice(name=char, value=char)
        for char in cowsay.char_names if current in char
    ][:25]
    

@client.event
async def on_ready():
    for guild in GUILDS:
        await tree.sync(guild=guild)
    cowsay.cow(f"I'm ready! GUILD_IDS={GUILD_IDS}")

client.run(TOKEN)
