# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from hyperlink import URL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# 2
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    url = URL.from_text(u'https://github.com/wtg/shuttletracker')
    better_url = url.replace(scheme=u'https', port=443)
    org_url = better_url.click(u'.')

    traccs_quotes = [
        ('Track? I myself prefer the more scrumptious'  + ' *tracc*' ),
        (org_url.to_text())
    ]

    if 'track' in message.content.lower() :
        response = random.choice(traccs_quotes)
        await message.channel.send(response)

bot.run(TOKEN)