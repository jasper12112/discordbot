import os
import random
import asyncio
import json
import praw

import discord
from discord.ext import commands as commandoo
from discord import utils
from discord.utils import get

#Reddit client
reddit = praw.Reddit(client_id=os.environ.get("REDDIT_ID"),
    client_secret=os.environ.get("REDDIT_SECRET"),
    user_agent="discordBot")

class Command(commandoo.Cog):

    #Init bot
    def __init__(self, bot):
        self.bot = bot

    #Command on ready
    @commandoo.Cog.listener()
    async def on_ready(self):
        print('Cog has been loaded!')

    @commandoo.command(aliases=['helpme'], help='sends all the commands')
    async def videohelp(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Developer")
        role2 = discord.utils.get(ctx.guild.roles, name="Admin")
        role3 = discord.utils.get(ctx.guild.roles, name="staff")
        roles = [role, role2, role3]

        hasRole = False

        for roleUsing in roles:
            if role in ctx.author.roles:
                hasRole = True

        if hasRole:
            embed = discord.Embed(
                    title="Video help",
                    description = 'How to use the addon: \n https://www.youtube.com/watch?v=NRe3kvABIOc&ab_channel=HR3Edits \nAddon installation video to world: \n https://streamable.com/nb6sr3',
                    colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have the right permissions for that")

    #Commands
    @commandoo.command(help='pong')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commandoo.command(aliases=['hello', 'hi', 'goodmorning'], help='greets you')
    async def greetings(self, ctx):
        user = ctx.message.author.name
        greets = [f'Hello {user}.', f'Greetings {user}.', f'Sir {user} I hope you have a wonderfull day.', f'Its nice to meet you {user}.']
        await ctx.send(random.choice(greets))

    @commandoo.command(aliases=['question', 'amiright', 'yes', 'no'], help='awnsers question to yes')
    async def yesorno(self, ctx):
        awnsers = ['yes thats certain', 'that is true', 'hmm must be sure', 'certainly', 'indeed motherfucker', 'that is so true']
        await ctx.send(f'{ctx.message.author.name} ' + random.choice(awnsers))

    @commandoo.command(aliases=['flipcoin', 'throw', 'coin', 'flip'], help='throws a coin random')
    async def coinflip(self, ctx):
        flipper=['head', 'tail']
        await ctx.send(f'{ctx.message.author.mention} '+ random.choice(flipper))
        
    @commandoo.command()
    async def download(self, ctx):
        embed = discord.Embed(title="Download link", description="The download link is: https://jaspervdijk63.github.io", colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)

    @commandoo.command(aliases=['reddit', 'gif'], help='sends a meme!')
    async def meme(self, ctx):
        imageUrls = []
        titles = []
        for submission in reddit.subreddit("memes").hot(limit=40):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                imageUrls.append(submission.url)
                titles.append(submission.title)
        random_post_number = random.randint(0, len(imageUrls))
        for i,image in enumerate(imageUrls):
            if i==random_post_number:
                embed = discord.Embed(
                    title=titles[i],
                    description = '',
                    colour = discord.Colour.blue()
                )
                embed.set_image(url=image)
                await ctx.send(embed=embed)

    @commandoo.command(aliases=['porn', 'nude'], help='sends a nsfw picture!')
    async def nsfw(self, ctx):
        if(ctx.channel.is_nsfw()):
            imageUrls = []
            titles = []
            for submission in reddit.subreddit("nsfw").hot(limit=40):
                if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                    imageUrls.append(submission.url)
                    titles.append(submission.title)
            random_post_number = random.randint(0, len(imageUrls))
            for i,image in enumerate(imageUrls):
                if i==random_post_number:
                    embed = discord.Embed(
                        title=titles[i],
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)
        else:
            await ctx.send("Please go to the NSFW Channel!")
            

    @commandoo.command(aliases=['punch'], help='Slap a user in the face!')
    async def slap(self, ctx, *, arg):
        to_slap = random.choice(ctx.guild.members)
        reason=arg
        if(to_slap == ctx.message.author):
            await ctx.send(f'{ctx.message.author.mention} slapped him self because he is heavily handicapped!')
            return
        await ctx.send(f'{ctx.message.author.mention} slapped {to_slap.mention} {reason}')

    @commandoo.command(help='Shows you your level!')
    async def level(self, ctx):
        with open('money.json', 'r') as f:
            users = json.load(f)
        user = ctx.message.author
        level = users[f'{user.id}']['level']
        await ctx.send(f'{ctx.message.author.mention}: {level}')

    @commandoo.command(aliases=['brawl', 'attack', 'match'], help='fight a player!')
    async def fight(self, ctx, arg1):
        health1 = 100
        health2 = 100
        player1 = ctx.message.author
        player2 = arg1
        await ctx.send(f'{player1.mention} will fight {player2}')
        player2 = ctx.message.mentions[0].name
        player1 = player1.name
        players= [player1, player2]
        while (True):
            player = random.choice(players)
            damage = random.randint(20, 50)
            if(player == player1):
                health2 = health2 - damage
                if(health2 <= 0):
                    health2 = 0
                await ctx.send(player1 + ' Smacks ' + player2 + f'\ndealing: {damage} damage! leaving them at {health2}\n _')
            else:
                health1 = health1 - damage
                if(health1 <= 0):
                    health1 = 0
                await ctx.send(player2 + ' Smacks ' + player1 + f'\ndealing: {damage} damage! leaving them at {health1}\n _')
            if(health1 <= 0):
                winner = player2
                await ctx.send(f'And the winner is {winner}')
                return
            elif(health2 <= 0):
                winner = player1
                await ctx.send(f'And the winner is {winner}')
                return
            await asyncio.sleep(1)
    
    @commandoo.command(aliases=['workingon', 'project'], help='Tells what project I am working on!')
    async def working(self, ctx):
        await ctx.send(ctx.message.author.mention + "I am Currently working on a Minecraft Addon (WORLD EDIT)")

    @commandoo.command(aliases=['embedhelp'], help='Sends a embed message!')
    async def embedMSG(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Developer")
        role2 = discord.utils.get(ctx.guild.roles, name="Admin")
        role3 = discord.utils.get(ctx.guild.roles, name="staff")
        roles = [role, role2, role3]

        hasRole = False

        for roleUsing in roles:
            if role in ctx.author.roles:
                hasRole = True

        if hasRole:
            embed = discord.Embed(
                    title="Info feedback, bugs",
                    description = 'If you find any bugs, please report them in <#770397512309407776>. \nDo you have feedback for the addon? Send it in <#770245107491536926>.',
                    colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have the right permissions for that!")

    @commandoo.command(aliases=['embedguide'], help="Sends a embed message with GUIDE")
    async def embedGuide(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Developer")
        role2 = discord.utils.get(ctx.guild.roles, name="Admin")
        role3 = discord.utils.get(ctx.guild.roles, name="staff")
        roles = [role, role2, role3]
        hasRole = False
        
        for roleUsing in roles:
            if role in ctx.author.roles:
                hasRole = True

        if hasRole:
            embed = discord.Embed(
                    title="Addon install",
                    description = 'Addon installation video to world: \n https://streamable.com/nb6sr3',
                    colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have the right permissions for that!")

    @commandoo.command(aliases=['d', 'down'], help="Sends download link")
    async def download(self, ctx):
        embed = discord.Embed(
            title="Download link",
            description = 'Download the addon here: https://jaspervdijk63.github.io',
            colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)

    @commandoo.command(aliases=['delmsg', 'delete'], help="Removes specified amount of messages")
    async def clear(self, ctx, number):
        totalMSG = int(number) + 1
        channel = ctx.message.channel
        deleted = await channel.purge(limit=totalMSG)
        channel = discord.utils.get(ctx.guild.channels, name="staff-chat")
        await channel.send('Deleted {} message(s)'.format(len(deleted)))



#Setup cog
def setup(bot):
    bot.add_cog(Command(bot))