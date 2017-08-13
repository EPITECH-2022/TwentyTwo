import discord
from discord.ext import commands

class Info:
    '''
    A collection of informative commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def topic(self, context):
        ''' Tells the channel's topic '''
        topic = context.message.channel.topic
        if topic in [None, '', ' ']:
            await self.bot.reply('there is no topic set here.')
        else:
            embed = discord.Embed(description=context.message.channel.topic)
            await self.bot.send_message(context.message.channel, embed=embed)
