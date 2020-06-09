# bot.py
import os
import requests
import re
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from hyperlink import URL

load_dotenv()
TOKEN = os.environ.get('DISCORD_MANBOT_TOKEN')
GUILD = os.environ.get('DISCORD_MANBOT_GUILD')

client = discord.Client()

bot = commands.Bot(command_prefix='>>')

@bot.command(name='man')
async def man(ctx, input_string: str):
    c = "http://s768147321.onlinehome.us/man/" + input_string
    r = requests.get(url=c)
    # p = re.sub('.\\x08', "", out)
    p = "Wrong input bub"
    if r.status_code == 200:
        p = (r.text[:1995] + '...') if len(r.text) > 1995 else r.text
    embed = discord.Embed(
        color = discord.Color.blue(),
        description = p
    )
    await ctx.send(embed=embed)


bot.run(TOKEN)
