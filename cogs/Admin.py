import sys

import discord
from discord.ext import commands

class Admin:
    '''
    A collection of administration commands
    '''
    def __init__(self, bot):
        self.bot = bot
        self.admin_roles = ['Administrateur']

    async def is_admin(self, user):
        # Hardcoded administrator priviledge for Tina#4153
        if user.discriminator in [4153, '4153']:
            return True

        if not hasattr(user, 'server'):
            msg = 'Admin commands can only be used by `Tina#4153` when outside of a server'
            await self.bot.send_message(user, msg)

        roles = user.server.roles
        i = len(roles) - 1
        while i > 0 and roles[i].name not in self.admin_roles:
            i -= 1
        if i != -1:
            admin = roles[i]
        if admin in user.roles:
            return True
        return False

    async def not_admin(self, message):
        await self.bot.add_reaction(message, '\N{FACE WITH NO GOOD GESTURE}')
        msg = 'User `{}` does not have administrator priviledge.'.format(message.author)
        await self.send_message(message.channel, msg)

    async def yes_admin(self, message):
        await self.bot.add_reaction(message, '\N{OK HAND SIGN}')

    async def check_admin(self, message):
        if not await self.is_admin(message.author):
            await self.not_admin(message)
            return False
        await self.yes_admin(message)
        return True

    @commands.command(pass_context=True)
    async def kill(self, context):
        if not await self.check_admin(context.message):
            return
        sys.exit()
