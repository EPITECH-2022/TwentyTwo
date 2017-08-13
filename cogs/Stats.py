import discord
from discord.ext import commands

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
        if where is None or where == 'status':
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

        if where == 'role':
            for role in serv.roles:
                stats[role.name] = 0
            for member in serv.members:
                for role in member.roles:
                    stats[role.name] += 1

        width = len(max(stats.keys(), key=len))
        f     = '{0:>%d}: {1}\n' % (width)
        msg = '```\n'
        for key, value in stats.items():
            msg += f.format(key, value)
        msg += '```'
        await self.bot.say(msg)
