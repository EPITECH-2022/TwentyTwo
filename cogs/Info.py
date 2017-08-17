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
        '''
        Tells the channel's topic
        '''
        topic = context.message.channel.topic
        if topic in [None, '', ' ']:
            await self.bot.reply('there is no topic set here.')
        else:
            embed = discord.Embed(description=context.message.channel.topic)
            await self.bot.send_message(context.message.channel, embed=embed)
            await self.bot.replied(context)

    @commands.command(pass_context=True)
    async def info(self, context, what: str = None):
        '''
        Gives info about something

        Usage   : info [[topic]]
        Options : topic = bot | commands | github | antilag
        '''
        embed = discord.Embed()
        if what != None:
            what  = what.casefold()
        if what in [None, 'bot']:
            content  = 'I am a bot made and run by `Tina#4153`.\n'
            content += 'Anyone can contribute to my code and add commands !\n'
            content += 'Please consider checking out the GitHub.'
            url      = 'https://github.com/EPITECH-2022/TwentyTwo'
            embed.add_field(name='Description', value=content)
            embed.add_field(name='GitHub',      value=url)
        elif what in ['command', 'commands']:
            header  = 'Commands are prefixed by a mention to `{}` or a `!`'.format(self.bot.user)
            admin   = '- kill (terminates / restarts the bot)\n'
            admin  += '- ban [@user] [["reason"]] [[delete message (days)]]\n'
            admin  += '- edit ["field"] ["value"] (edit the bot account)\n'
            admin  += '- clean [[limit=100]] (removes bot messages)\n'
            admin  += '- purge [[limit=100]] [[@user]]\n'
            admin  += '- set [config flag] [[value]]\n'
            admin  += '- check [config flag]\n'
            admin  += '- playing [text] (edit bot status)'
            fun     = '- hello, - hi, - help\n'
            fun    += '- age [[@user]], - joined [[@user]]\n'
            fun    += '- emoji | ri ["text to convert to emoji"]\n'
            fun    += '- decode ["text"]\n'
            fun    += '- trad ["language (2 characters)"] ["text"]\n'
            fun    += '- pronunciation | pron ["text"]\n'
            fun    += '- wiki [text]'
            stats   = '- enum [[everyone | status | role | game | here]]\n'
            stats  += '- whoplays ["partial matching text"]'
            info    = '- topic\n'
            info   += '- info [bot | commands | github | antilag]'
            embed.add_field(name='Usage', value=header)
            embed.add_field(name='Admin', value=admin)
            embed.add_field(name='Fun',   value=fun)
            embed.add_field(name='Stats', value=stats)
            embed.add_field(name='Info',  value=info)
        elif what in ['git', 'github', 'Github', 'GitHub']:
            github  = 'GitHub is an online GUI and augmentation for using Git.\n'
            github += 'You can use GitHub to read the code, send pull requests...'
            git     = 'Git is an old (but still maintained) free versioning software.'
            link    = 'https://github.com/EPITECH-2022/TwentyTwo'
            embed.add_field(name='GitHub', value=github)
            embed.add_field(name='Git',    value=git)
            embed.add_field(name='Check this bot on GitHub', value=link)
        elif what in ['lag', 'lagging', '3g', 'h+', 'doublon', 'anti-lag', 'antilag']:
            lagging   = 'Discord has no native anti lag. That means when someone'
            lagging  += ' is on a slow connection, there is a potential risk that'
            lagging  += ' the message he is trying to send will be sent multiple'
            lagging  += ' times. That is no good.'
            anti_lag  = 'To prevent this, this bot is designed with an automatic'
            anti_lag += ' message purging. On every message it will check a very'
            anti_lag += ' specific predicate on the 10 previous messages. Here is'
            anti_lag += ' the specs :\n'
            anti_lag += '- Message has the same content and\n'
            anti_lag += '- Message has less than 20 seconds difference and\n'
            anti_lag += '- Message has been posted by the same user and\n'
            anti_lag += '- Message has not the same unique ID.'
            embed.add_field(name='Lagging',  value=lagging)
            embed.add_field(name='Anti-Lag', value=anti_lag)
        else:
            return
        await self.bot.send_message(context.message.channel, embed=embed)
        await self.bot.replied(context)
