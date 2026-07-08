#!/usr/bin/env python3

import datetime
import os

import cowsay # pyright: ignore[reportMissingTypeStubs]
import discord
import dotenv

dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]
GUILD_IDS = [int(guild_id) for guild_id in os.environ["GUILD_IDS"].split(",")]
GUILDS = [discord.Object(guild_id) for guild_id in GUILD_IDS]
MESSAGE_LENGTH_MAX = 2000

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

def get_truncated_cowsay(character: str, say: str, backoff: int = 1) -> str:
    message = f"```\n{cowsay.get_output_string(character, say)}\n```"
    if len(message) <= MESSAGE_LENGTH_MAX:
        return message

    truncate_by = len(message) - MESSAGE_LENGTH_MAX
    say = say[:-1 - truncate_by - len("...") - backoff] + "..."
    return get_truncated_cowsay(character, say, backoff*2)

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

    if not character in cowsay.CHARS:
        character = "cow"
        text = f"{character} does not exist as a character. Try the following: {', '.join(cowsay.char_names)}."

    await interaction.response.send_message(get_truncated_cowsay(character, text))

@_cowsay.autocomplete("character")
async def character_autocomplete(
        interaction: discord.Interaction,
        current: str,
) -> list[discord.app_commands.Choice[str]]:
    current = current.lower()
    return [
        discord.app_commands.Choice(name=char, value=char)
        for char in cowsay.char_names if current in char
    ][:25]
    

@client.event
async def on_ready():
    for guild in GUILDS:
        await tree.sync(guild=guild)
    cowsay.cow(f"I'm ready! GUILD_IDS={GUILD_IDS}") # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

client.run(TOKEN)
