import discord
from discord.ext import commands

def format_keyvalues(dictionary):
    r     = ''
    width = len(max(dictionary.keys(), key=len))
    f     = '{0:>%d}: {1}\n' % (width)
    for key, value in dictionary.items():
        if isinstance(value, list):
            r += f.format(key, '{}/{}'.format(value[0], value[1]))
        else:
            r += f.format(key, value)
    return r


class Stats:
    '''
    A collection of commands to get statistics
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='enum', aliases=['enumerate'], no_pm=True)
    async def _enumerate(self, context, option: str = None):
        '''
        Count how many people are on the server.

        Count how many people are on the server or sort them by different predicates.

        Usage   : enum [[option]]
        Options : [everyone | status | role | game | here]
        '''
        from collections import defaultdict
        stats  = defaultdict(int)
        serv   = context.message.server
        if option != None:
            option = option.casefold()
        if option in [None, 'everyone']:
            stats['Members'] = len(serv.members)

        elif option in ['here', 'present', 'connected']:
            stats['Total']     = 0
            stats['Connected'] = 0
            for member in serv.members:
                if not member.bot:
                    if member.status == discord.Status.offline:
                        stats['Offline'] += 1
                    else:
                        stats['Connected'] += 1
            stats['Total'] = stats['Connected'] + stats['Offline']

        elif option in ['status', 'statuses']:
            stats['Connected'] = 0
            for member in serv.members:
                if not member.bot:
                    stats['Online']         += member.status == discord.Status.online
                    stats['Idle']           += member.status == discord.Status.idle
                    stats['Do not disturb'] += member.status == discord.Status.dnd
                    stats['Playing']        += member.game != None
                    stats['Streaming']      += member.game !=None and member.game.type == 1
                    stats['Offline']        += member.status == discord.Status.offline
            stats['Connected'] = stats['Online'] + stats['Idle'] + stats['Do not disturb']
            stats['Total'] = stats['Connected'] + stats['Offline']

        elif option in ['role', 'roles']:
            for role in serv.roles:
                # Sorting roles in server's order
                stats[role.name] = [0, 0]
            for member in serv.members:
                for role in member.roles:
                    stats[role.name][0] += member.status != discord.Status.offline
                    stats[role.name][1] += 1

        elif option in ['game', 'games']:
            for member in serv.members:
                if member.game != None and not member.bot:
                    stats['Playing']        += 1
                    stats[member.game.name] += 1

        elif option in ['rank', 'ranks', 'campus']:
            for role in serv.roles:
                if role.name in self.bot.rank_whitelist:
                    stats[role.name] = 0
            for member in serv.members:
                for role in member.roles:
                    if role.name in self.bot.rank_whitelist:
                        stats[role.name] += 1

        else:
            return
        msg = '```\n'
        msg += format_keyvalues(stats)
        msg += '```'
        await self.bot.say(msg)
        await self.bot.replied(context)

    @commands.command(pass_context=True, name='whoplays', no_pm=True)
    async def _who_plays(self, context, game:str = None):
        '''
        Tells who play a given game. (partial matching)

        Case insensitive, ignoring unicode matching.
        i.e.: "bibi" can match "Âbabîbîbou"

        Usage : whoplays [text]
        '''
        if game is None:
            await self.bot.reply('Please input a game name.')
            return
        found = []
        game = game.casefold()
        for member in context.message.server.members:
            if member.game != None and game in member.game.name.casefold():
                found.append(member)

        msg  = '```'
        msg += 'Total: {}\n'.format(len(found))
        for member in found:
            msg += '- {} ({})\n'.format(member, member.game)
        msg += '```'
        await self.bot.say(msg)
        await self.bot.replied(context)
