import os
import random
import asyncio
import json
import praw

import discord
from discord.ext import commands
from discord import utils
from discord.utils import get

#Reddit client
reddit = praw.Reddit(client_id=os.environ.get("REDDIT_ID"),
    client_secret=os.environ.get("REDDIT_SECRET"),
    user_agent="discordBot")

class Trivia(commands.Cog):

    #Init bot
    def __init__(self, bot):
        self.bot = bot

    #Command on ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog has been loaded!')

    #Commands
    @commands.command(help='trivia question')
    async def testtrivia(self, ctx):
        await ctx.send('Guess a number between 1 and 5!')

        def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 5)

        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send('Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('You are right!')

        else:
            await ctx.send('Oops. It is actually {}.'.format(answer))

#Setup cog
def setup(bot):
    bot.add_cog(Trivia(bot))