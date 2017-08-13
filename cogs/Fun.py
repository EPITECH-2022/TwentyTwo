import discord
from discord.ext import commands

class Fun:
    '''
    A collection of commands to rolls dices, send cats, and drop mixtapes (probably)
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self):
        ''' says the robot '''
        await self.bot.reply('hi!')

    @commands.command()
    async def hi(self):
        ''' says the IA '''
        await self.bot.reply('hello!')

    @commands.command(pass_context=True)
    async def age(self, context, member: discord.Member = None):
        ''' Tells the age of a Discord account '''
        if member is None:
            member = context.message.author
        await self.bot.say('`{0}` joined Discord at {0.created_at}'.format(member))

    @commands.command()
    async def help(self):
        await self.bot.reply('ask `Tina#4153`')
