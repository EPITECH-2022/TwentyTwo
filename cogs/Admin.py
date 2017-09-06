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
        if context.bot.is_owner(context.message.author):
            return True

        if not hasattr(context.message, 'server'):
            return False

        admin_roles = []
        for role in context.message.server.roles:
            if role.name in context.bot.admin_roles:
                admin_roles.append(role)
        i = len(context.message.author.roles) - 1
        while i >= 0 and context.message.author.roles[i] not in admin_roles:
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
        '''
        Edit the bot account

        Usage   : edit [field] [value]
        Fields  : username
        Values  : "string"
        '''
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
        except discord.errors.NotFound:
            pass
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
        except discord.errors.NotFound:
            pass
        except Exception as e:
            await self.bot.report(context, e)

    @commands.command(name='set', pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def _set(self, context):
        content = self.bot.get_text(context)
        words   = content.split()
        length  = len(words)
        if length == 0:
            await self.bot.reply('please input a flag to set.')
            await self.bot.doubt(context)
        flag = words[0]
        if flag not in self.bot.config.keys():
            await self.bot.reply('please input a valid flag. Possible values:\n'
                               + 'verbose | bleeding | reactive')
            await self.bot.doubt(context)
            return
        if len(words) > 1:
            value = words[1].casefold()
            if   value == 'true':
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

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def playing(self, context):
        content = self.bot.get_text(context)
        game = discord.Game(name=content)
        await self.bot.change_presence(game=game)
        await self.bot.ok(context)

    @commands.command(pass_context=True)
    async def rank(self, context, role: str = None, user: discord.Member = None):
        words = self.bot.get_text(context).split()
        # if there is no word in the command text we ignore the command
        if len(words) == 0:
            await self.bot.reply('please specify a rank role to use.')
            await self.bot.doubt(context)
            return
        # we set the target as the author and default to not an admin
        target = context.message.author
        admin  = Admin.is_admin(context)
        # if there is a second word and it is
        if len(words) > 1 and user is not None:
            if not admin:
                await self.bot.reply('you must be an administrator to set'
                + 'someone else\'s rank.')
                await self.doubt(context)
                return
            target = user
        value = words[0].casefold()
        # we build a whitelist based on the sever roles and the bot self whitelist
        server_rank_whitelist = []
        for role in context.message.server.roles:
            if role.name in self.bot.rank_whitelist:
                server_rank_whitelist.append(role)
        # to ensure the user has one and only rank we check his ranks
        # if we found out he already has one and the command was not initiated
        # by an admin, we return with an error, else we unset the other ranks
        for role in target.roles:
            if role in server_rank_whitelist:
                if not admin:
                    await self.bot.reply('you can not override your rank roles.\n'
                    + 'If you think this is an error, please contact an Admin.')
                    await self.bot.doubt(context)
                    return
                try:
                    await self.bot.remove_roles(target, role)
                    self.bot.log('Removed role {} from {}'.format(role, target))
                except discord.errors.Forbidden as e:
                    await self.bot.report(context, e)
        # we search the whitelist for a role which's name = the command option
        i = len(server_rank_whitelist) - 1
        while i >= 0 and server_rank_whitelist[i].name.casefold() != value:
            i -= 1
        # no matching role found, we tell the user his option is not whitelisted
        if i < 0:
            await self.bot.reply('the rank role you specified is not'
            + ' whitelisted on this server.\n'
            + 'If you think this is an error, please contact an Admin.')
            await self.bot.doubt(context)
            return
        # else we try to add the roles and catch for Discord Forbidden error
        try:
            await self.bot.add_roles(target, server_rank_whitelist[i])
            await self.bot.ok(context)
        except discord.errors.Forbidden as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True)
    async def ranks(self, context):
        server_rank_whitelist = []
        for role in context.message.server.roles:
            if role.name in self.bot.rank_whitelist:
                server_rank_whitelist.append(role)
        if len(server_rank_whitelist) == 0:
            await self.bot.reply('there are no rank roles on this server.')
            await self.bot.shrug(context)
        msg  = 'This is a list of the roles that counts as "rank role" on this server.\n'
        msg += 'What we call a "rank role" is a Discord role that is used as a'
        msg += ' rank. Meaning you can only have one role from the ranks list.\n'
        msg += '```\n'
        for role in server_rank_whitelist:
            msg += '{0.name}\n'.format(role)
        msg += '```'
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    @commands.check(is_admin)
    async def erase(self, context, limit: int = 100, user: discord.Member = None):
        if user is None:
            await self.bot.reply('please specify an user.')
            await self.bot.say('Usage: erase [limit] [@user]')
            await self.bot.doubt(context)
            return
        def is_user(message):
            return message.author == user
        try:
            deleted = 0
            for channel in context.message.server.channels:
                try:
                    deleted_now = await self.bot.purge_from(channel, limit=limit, check=is_user)
                    deleted += len(deleted_now)
                except discord.errors.HTTPException as e:
                    # if we encounter a message that is > 14 days old we can not purge it
                    # (error code 50034)
                    # we simply skip this channel
                    if e.code == 50034:
                        pass
                    else:
                        raise e
            await self.bot.say('Deleted {} messages.'.format(deleted))
            await self.bot.ok(context)
        except discord.errors.NotFound:
            pass
        except discord.errors.Forbidden as e:
            await self.bot.report(context, e)
