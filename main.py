import os

import cowsay
import discord
import discord_slash

client = discord.ext.commands.Bot(intents=discord.Intents(), command_prefix="!")
slash = discord_slash.SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('cowsay ready!')

options = options=[
    discord_slash.utils.manage_commands.create_option(
        name="animal", description="Pick your animal spirit!" , option_type=3, required=True, choices = [
            discord_slash.utils.manage_commands.create_choice(name=animal, value=animal) for animal in cowsay.char_names
        ]
    ),
    discord_slash.utils.manage_commands.create_option(
        name="message", description="What do you want to say?" , option_type=3, required=True
    )
]

guild_ids = [int(guild_id) for guild_id in os.getenv('GUILD_IDS').split(",")]

@slash.slash(name="cowsay", guild_ids=guild_ids, options=options)
async def cowsayfunc(ctx, animal: str, message: str):
    await ctx.send(content=f'```\n{cowsay.get_output_string(animal, message)}```\n')

client.run(os.getenv('TOKEN'))
