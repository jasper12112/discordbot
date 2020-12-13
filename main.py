import os
import random
import asyncio
import json
import socket

#from keep_alive import keep_alive
from threading import Thread

import discord
from discord.ext import commands as commandoo
from discord import utils
from discord.utils import get
from discord.ext.commands.cooldowns import BucketType

import threading

#Get Token
token = os.environ.get("DISCORD_BOT_SECRET")

#Prefix
intents = discord.Intents.all()
bot = commandoo.Bot(command_prefix='!', intents=intents)

#Bot Ready
@bot.event
async def on_ready():
    for filename in os.listdir(f"./cogs"):
        if filename.endswith(f".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f'cog: {filename[:-3]} has been loaded!')
    for guild in bot.guilds:
        print(f'{bot.user} is connected to the following guild:\n'
		      f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

        role = discord.utils.get(guild.roles, name="member")
        for member2 in guild.members:
            if role not in member2.roles:
                await member2.add_roles(role)
                print(f'Added role to {member2.name}')


rate = 1

per = 10

t = BucketType.default


#Member Join
@bot.event
async def on_member_join(member):
    print('member joined')
    await member.add_roles(
        discord.utils.get(member.guild.roles, name="member"))
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!')

    with open('money.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('money.json', 'w') as f:
        json.dump(users, f)


#On Message
@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('money.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('money.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(
            'This command is on a %.2fs cooldown' % error.retry_after)
    else:
        print("Error")
    raise error


#Update level en exp
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


#Add EXP
async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


#Level UP
async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience**(1 / 4))
    if lvl_start < lvl_end:
        channelsendto = bot.get_channel(716394570220437555)
        await channelsendto.send(
            f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


@bot.command(help='trivia question')
@commandoo.cooldown(1, 30)
async def trivia(ctx):
    try:
        await ctx.send('Guess a number between 1 and 5!')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 5)

        try:
            guess = await bot.wait_for(
                'message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(
                'Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            with open('money.json', 'r') as f:
                users = json.load(f)
            await add_experience(users, ctx.author, 100)
            await ctx.send('You are right, added 100 experience!')
        else:
            await ctx.send('Oops. It is actually {}.'.format(answer))
    except discord.ext.commands.errors.CommandOnCooldown:
        ctx.send('You are in a cooldown!')


#Start webapp
#keep_alive()
#Start bot
bot.run(token)