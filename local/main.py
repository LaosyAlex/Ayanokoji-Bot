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