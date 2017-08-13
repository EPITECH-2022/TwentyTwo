import discord
from discord.ext import commands

def format_keyvalues(dictionary):
    r     = ''
    width = len(max(dictionary.keys(), key=len))
    f     = '{0:>%d}: {1}\n' % (width)
    for key, value in dictionary.items():
        r += f.format(key, value)
    return r


class Stats:
    '''
    A collection of commands to get statistics
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='enum')
    async def _enumerate(self, context, where: str = None):
        stats = {}
        serv  = context.message.server
        if where is None or where == 'everyone':
            stats['Members'] = len(serv.members)

        if where == 'status' or where == 'statuses':
            stats['Connected']      = 0
            stats['Online']         = 0
            stats['Idle']           = 0
            stats['Do not disturb'] = 0
            stats['Offline']        = 0
            for member in serv.members:
                stats['Online']         += member.status == discord.Status.online
                stats['Idle']           += member.status == discord.Status.idle
                stats['Do not disturb'] += member.status == discord.Status.dnd
                stats['Offline']        += member.status == discord.Status.offline
            stats['Connected'] = stats['Online'] + stats['Idle'] + stats['Do not disturb']
            stats['Total'] = stats['Connected'] + stats['Offline']

        if where == 'role' or where == 'roles':
            for role in serv.roles:
                stats[role.name] = 0
            for member in serv.members:
                for role in member.roles:
                    stats[role.name] += 1

        msg = '```\n'
        msg += format_keyvalues(stats)
        msg += '```'
        await self.bot.say(msg)

    @commands.command(pass_context=True, name='whoplays')
    async def _who_plays(self, context, game:str = None):
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
