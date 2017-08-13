import json, os.path, asyncio, datetime

import discord
from discord.ext import commands

import config
import cogs
from Verifier import Verifier

def main():

    # define bot
    bot = Bot(description=config.description, verbose=config.verbose, bleeding=config.bleeding)
    bot.add_cog(cogs.Fun  (bot))
    bot.add_cog(cogs.Stats(bot))
    bot.add_cog(cogs.Info (bot))
    bot.add_cog(cogs.Admin(bot))

    # launch bot
    try:
        bot.run(config.token)
    except discord.errors.LoginFailure as e:
        print(e, end='\n\n')

class Bot(commands.Bot):

    def __init__(self, verbose=False, bleeding=False, *args, **kwargs):
        # Rewrite the command_prefix flag to force mention
        super().__init__(*args, command_prefix=commands.when_mentioned_or('!'), **kwargs)

        self.admins      = []
        self.admin_roles = ['Administrateur']
        self.verbose     = verbose
        self.bleeding    = bleeding

    def log(self, txt):
        if self.verbose:
            print(txt)

    def is_owner(self, user):
        return user.name + '#' + str(user.discriminator) == 'Tina#4153'

    def get_text(self, context):
        return context.message.content[(len(context.prefix + context.invoked_with)) + 1:]

    async def report(self, context, error):
        await self.add_reaction(context.message, '\N{THINKING FACE}')
        msg   = 'Error !'
        embed = discord.Embed(description=str(error), colour=discord.Colour.orange())
        await self.send_message(context.message.channel, msg, embed=embed)

    async def ok(self, context):
        await self.add_reaction(context.message, '\N{OK HAND SIGN}')

    async def on_ready(self):
        self.log('Logged as {}#{}'.format(self.user.name, self.user.id))
        self.log('My boty is ready')



    @asyncio.coroutine
    def on_message(self, message):
            def anti_lag(message2):
                # same id = not a lag
                if message.id == message2.id:
                    return False
                # different author = not a lag
                if message.author != message2.author:
                    return False
                # more than 2 minutes delta = not a lag
                if message.timestamp - message2.timestamp > datetime.timedelta(0, 120):
                    return False
                # same content = a lag, not same content = not a lag
                if message.content == message2.content:
                    return message.embeds == message2.embeds
            # call purge check anti_lag on every message
            yield from self.purge_from(message.channel, limit=10, check=anti_lag)
            # process commands
            yield from self.process_commands(message)

    async def on_member_join(self, member):
        if self.bleeding:
            self.log('Initiating verification procedure for user "{}".'.format(member.name))
            msg  = 'Please send !register followed by your EPITECH mail adress\n'
            msg += 'i.e.: ```!register yournam_e@epitech.eu```\n'
            msg += 'It has to be an EPITECH address, any other address will not be accepted'
            await self.send_message(member, msg)
            Verifier.add(member)

if __name__ == '__main__':
    main()
