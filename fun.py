import discord
from discord.ext import commands

class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello():
        await self.bot.reply('Hi!')
    async def hi():
        await self.bot.reply('Hello!')
