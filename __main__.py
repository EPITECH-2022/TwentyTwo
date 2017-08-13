import json, os.path, asyncio
import discord
from discord.ext import commands

import config
import cogs
from Verifier import Verifier

def main():

    # define bot
    bot = Bot(description=config.description, verbose=config.verbose, bleeding=config.bleeding)
    bot.remove_command('help')
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
            yield from self.process_commands(message)

    async def on_member_join(self, member):
        if self.bleeding:
            self.log('Initiating verification procedure for user "{}".'.format(member.name))
            msg  = 'Please send regiser followed by your EPITECH mail adress\n'
            msg += 'i.e.: ```register yournam_e@epitech.eu```\n'
            msg += 'It has to be an EPITECH adress, any other adress will not be accepted'
            await self.send_message(member, msg)
            Verifier.add(member)

if __name__ == '__main__':
    main()
