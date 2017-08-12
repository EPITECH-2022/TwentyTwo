import discord
from discord.ext import commands

class Fun:

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
