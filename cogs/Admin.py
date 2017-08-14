import discord
from discord.ext import commands

class Admin:
    '''
    A collection of administration commands
    '''
    def __init__(self, bot):
        self.bot = bot

    async def not_admin(self, message):
        await self.bot.add_reaction(message, '\N{FACE WITH NO GOOD GESTURE}')
        msg = 'User `{}` does not have administrator priviledge.'.format(message.author)
        await self.bot.send_message(message.channel, msg)

    def is_admin(context):
        user = context.message.author
        if context.bot.is_owner(user):
            return True

        if not hasattr(user, 'server'):
            return False

        admin_roles = []
        for role in context.message.server.roles:
            if role.name in context.bot.admin_roles:
                admin_roles.append(role)
        i = len(user.roles) - 1
        while i >= 0 and user.roles[i] not in admin_roles:
            i -= 1
        return i != -1

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def kill(self, context):
        import sys
        await self.bot.ok(context)
        if self.bot.config['reactive']:
            await self.bot.say('\N{WINKING FACE}\N{PISTOL}')
        sys.exit()

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @commands.check(is_admin)
    async def ban(self, context, user: discord.Member = None, reason: str = None, delete: int = 0):
        if user is None:
            await self.bot.reply('please set a user to sentence.')
            return
        try:
            embed = discord.Embed(title="Ban notice", description='Reason: {}'.format(reason), colour=discord.Colour.dark_red())
            embed.set_author(name=context.message.server)
            await self.bot.send_message(user, embed=embed)
            await self.bot.ban(user, delete_message_days=delete)
            await self.bot.ok(context)
        except Exception as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def edit(self, context, field: str = None, value: str = None):
        if field is None or value is None:
            await self.bot.reply('Please set a field/value.')
            await self.bot.doubt(context)
            return
        username = None
        #TODO avatar   = None
        if field == 'username':
            username = value
        try:
            await self.bot.edit_profile(username=username)
            await self.bot.ok(context)
        except Exception as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True, aliases=['cls', 'clear'], hidden=True)
    @commands.check(is_admin)
    async def clean(self, context, limit: int = 100):
        def predicate(message):
            return message.author == self.bot.user
        try:
            message = context.message
            deleted = await self.bot.purge_from(message.channel, limit=limit, check=predicate)
            await self.bot.say('Deleted {} messages.'.format(len(deleted)))
            await self.bot.ok(context)
        except Exception as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def purge(self, context, limit: int = 100, user: discord.Member = None):
        is_user  = None
        if user != None:
            def is_user(message):
                return message.author == user
        try:
            message = context.message
            deleted = await self.bot.purge_from(message.channel, limit=limit, check=is_user)
            await self.bot.say('Deleted {} messages.'.format(len(deleted)))
            await self.bot.ok(context)
        except Exception as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def set(self, context):
        content = self.bot.get_text(context)
        words   = content.split()
        length  = len(words)
        if length == 0:
            await self.bot.reply('please input a flag to set.')
            await self.bot.doubt(context)
        flag    = words[0]
        if flag not in self.bot.config.keys():
            await self.bot.reply('please input a valid flag. Possible values:\n'
                            + 'verbose | bleeding | reactive')
            await self.bot.doubt(context)
            return
        if len(words) > 1:
            value = words[1].casefold()
            if  value == 'true':
                def switch(value):
                    return True
            elif value == 'false':
                def switch(value):
                    return False
            else:
                def switch(value):
                    return not value
        else:
            def switch(value):
                return not value
        self.bot.config[flag] = switch(self.bot.config[flag])
        await self.bot.say('Set flag {} to {}'.format(flag, self.bot.config[flag]))
        await self.bot.ok(context)

    @commands.command(name='check', pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def _check(self, context):
        content = self.bot.get_text(context)
        words   = content.split()
        if len(words) == 0:
            self.bot.reply('please input a flag to set.')
            self.bot.doubt(context)
        flag    = words[0]
        if flag not in self.bot.config.keys():
            await self.bot.reply('please input a valid flag. Possible values:\n'
                            + 'verbose | bleeding | reactive')
            return
        await self.bot.say('Value of {} : {}'.format(flag, self.bot.config[flag]))
        await self.bot.replied(context)
