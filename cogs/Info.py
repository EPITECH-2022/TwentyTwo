import discord
from discord.ext import commands

class Info:
    '''
    A collection of informative commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def topic(self, context):
        ''' Tells the channel's topic '''
        if context.message.channel.topic == '':
            await self.bot.reply('There is no topic set here.')
        else:
            await self.bot.say('"{0.message.channel.topic}"'.format(context))
