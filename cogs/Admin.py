import discord
from discord.ext import commands

class Admin:
    '''
    A collection of administration commands
    '''
    def __init__(self, bot):
        self.bot = bot
        self.admin_roles = ['Administrateur']

    def is_admin(self, user):
        # Hardcoded administrator priviledge for Tina#4153
        if user.discriminator in [4153, '4153']:
            return True

        if not hasattr(user, 'server'):
            await self.bot.reply('Admin commands can only be used by `Tina#4153` when outside of a server')

        roles = user.server.roles
        i = len(roles) - 1
        while i > 0 and roles[i].name not in self.admin_roles:
            i -= 1
        if i != -1:
            admin = roles[i]
        if admin in user.roles:
            return True
        return False
