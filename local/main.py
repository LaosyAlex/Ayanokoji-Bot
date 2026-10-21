#Note to self: actually try to understand what the hell you are doing later instead of copying and pasting shit from a tutorial

import discord
from discord.ext import commands
import logging #No idea of any of the logging stuff btw, add that in the list of thigns to review
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf=8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.content.startswith('!'):
        return

bot.run(token, log_handler=handler, log_level=logging.DEBUG)