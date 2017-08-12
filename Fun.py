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
        await self.bot.reply('Hi!')

    @commands.command()
    async def hi(self):
        ''' says the IA '''
        await self.bot.reply('Hello!')

    @commands.command(pass_context=True)
    async def age(self, ctx, member: discord.Member = None):
        ''' tells the age of a Discord account '''
        if member is None:
            member = ctx.message.author
        await self.bot.say('{0} joined Discord at {0.created_at}'.format(member))
