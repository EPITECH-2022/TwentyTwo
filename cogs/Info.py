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

    @commands.command(pass_context=True)
    async def info(self, context, what: str = None):
        ''' Gives info about something '''
        embed = discord.Embed()
        if what in [None, 'bot']:
            content  = 'I am a bot made and run by `Tina#4153`.\n'
            content += 'Anyone can contribute to my code and add commands !\n'
            content += 'Pleaase consider checking out the GitHub.'
            url      = 'https://github.com/EPITECH-2022/TwentyTwo'
            embed.add_field(name='Description', value=content)
            embed.add_field(name='GitHub',      value=url)
        await self.bot.send_message(context.message.channel, embed=embed)
