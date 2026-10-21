import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv 
import os
from yt_dlp import YoutubeDL
from instaloader import Instaloader, Post
from pathlib import Path #turns strings to path objects (I think)
import subprocess #allows to run command line inputd
from PIL import Image #Pillow, for image compression
import requests
import http.cookiejar
from urllib.parse import urlparse
import json
import asyncio
import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

CONFIG_FILE = Path("config.json")

handler = logging.FileHandler(filename='discord.log', encoding='utf=8', mode='w')
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def setChannel(ctx, *, msg):
    if get_channel_id(ctx.guild.id) != None:
        Target_Channel = await bot.fetch_channel(get_channel_id(ctx.guild.id))
    else:
        Target_Channel = None

    try:
        data = load_data()
        guild_id = str(ctx.guild.id)

        if guild_id not in data:
            data[guild_id] = {}

        channel_id = int(msg)
        channel = await bot.fetch_channel(channel_id)
        if Target_Channel == None:
            await ctx.reply(f"Setting channel from 'Nothing' to '{channel.name}':'{channel.id}'")
        else:
            await ctx.reply(f"Setting channel from '{Target_Channel}' to '{channel.name}':'{channel.id}'")
        Target_Channel = channel

        data[guild_id]["channel_id"] = Target_Channel.id
        save_data(data)

        print('set')
    except discord.NotFound:
        await ctx.reply(f"Channel '{channel_id}' does not exist")
        print('not found')
    except discord.Forbidden:
        await ctx.reply(f"Bot cannot access channel '{channel_id}'")
        print('forbidden')
    except discord.HTTPException:
        await ctx.reply(f"Channel '{channel_id}' results in an unknown error")
        print('unknown error')
    except Exception as e:
        await ctx.reply(f"Error: {e}")

@bot.command()
async def currentChannel(ctx):
    if get_channel_id(ctx.guild.id) != None:
        Target_Channel = await bot.fetch_channel(get_channel_id(ctx.guild.id))
    else:
        Target_Channel = None

    if Target_Channel == None:
        await ctx.reply(f"None/Not set")
    else:
        await ctx.reply(f"{Target_Channel.name}: {Target_Channel.id}")

@bot.event
async def on_guild_join(guild):
    #initializes json to default settings
    data = load_data()

    data[str(guild.id)] = {
        "channel_id": None
    }

    save_data(data)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.command()
async def retry(ctx):
    if get_channel_id(ctx.guild.id) != None:
        Target_Channel = await bot.fetch_channel(get_channel_id(ctx.guild.id))
    else:
        Target_Channel = None

    if Target_Channel is None or ctx.channel.id != Target_Channel.id or ctx.message.reference is None:
        await ctx.message.reply("Reply to a message in the right channel to retry.")
        return
    
    replied_message = await ctx.channel.fetch_message(
        ctx.message.reference.message_id
    )

    await processURL(replied_message)

@bot.event
async def on_message(message):
    if get_channel_id(message.guild.id) != None:
        Target_Channel = await bot.fetch_channel(get_channel_id(message.guild.id))
    else:
        Target_Channel = None

    if message.author == bot.user:
        return
    
    await bot.process_commands(message) # let commands run first

    if message.content.startswith('!'): # prevents commands from reaching code
        return

    if Target_Channel is None or message.channel.id != Target_Channel.id: # only restrict normal messages
        print('not right channel')
        return
    
    await processURL(message)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)