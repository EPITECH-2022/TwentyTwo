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
        if what in ['command', 'commands']:
            header  = 'Commands are prefixed by a mention to `{}` or a `!`'.format(self.bot.user)
            admin   = '- kill\n'
            admin  += '- ban [@user] [["reason"]] [[delete message (days)]]\n'
            admin  += '- edit ["field"] ["value"] (edit the bot account)'
            fun     = '- hello, - hi, - help\n'
            fun    += '- age [[@user]]'
            stats   = '- enum [everyone | status | role | game | here]\n'
            stats  += '- whoplays ["partial matching text"]'
            info    = '- topic\n'
            info   += '- info [bot | command]'
            embed.add_field(name='Usage', value=header)
            embed.add_field(name='Admin',  value=admin)
            embed.add_field(name='Fun',    value=fun)
            embed.add_field(name='Stats',  value=stats)
            embed.add_field(name='Info',   value=info)
        await self.bot.send_message(context.message.channel, embed=embed)
