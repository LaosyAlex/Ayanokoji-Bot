#Note to self: actually try to understand what the hell you are doing later instead of copying and pasting shit from a tutorial

import discord
from discord.ext import commands
import logging #No idea of any of the logging stuff btw, add that in the list of thigns to review
from dotenv import load_dotenv
import os
import utils
from generic import Generic

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
    if message.author == bot.user or message.author.id == 1495334750905434283:
        print("Bot message.")
        return

    await bot.process_commands(message)

    if message.content.startswith('!'):
        return

    if any(domains in message.content for domains in utils.gif_domains) or ".gif" in message.content:
        print("reaction gif detected.")
        return

    print("message detected")
    if "https://" in message.content:
        link = utils.get_link(message.content)

        content = Generic(link)
        text, attach = content.process()

        files = [discord.File(path) for path in attach]

        if len(text) > 1:
            replyMSG = message
            for index, value in enumerate(text):
                if index < len(text) - 1:
                    replyMSG = await replyMSG.reply(value + "...")
                else:
                    replyMSG = await replyMSG.reply(value, files=files)
        else:
            await message.reply(text[0], files=files)

        del content

        print("Done!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)