import json, os.path
import discord
from discord.ext import commands

from Fun import Fun

def main():

    # variables
    config_file = 'config.json'

    # load config
    with open(config_file) as f:
        config = json.load(f)

    # split config
    description, token = config['description'], config['token']
    verbose, token     = config['verbose'], config['bleeding']

    # define bot
    bot = Bot(description=description, verbose=verbose, bleeding=bleeding)
    bot.add_cog(Fun(bot))

    # launch bot
    bot.run(token)

class Bot(commands.Bot):

    def __init__(self, *args, verbose=False, bleeding=False, **kwargs):
        # Rewrite the command_prefix flag to force mention
        super().__init__(*args, command_prefix=commands.when_mentioned, **kwargs)

        self.admins  = []
        self.verbose  = verbose
        self.bleeding = bleeding

    def log(self, txt):
        if self.verbose:
            print(txt)

    async def on_ready(self):
        self.log('Logged as {}#{}'.format(self.user.name, self.user.id))
        self.log('My boty is ready')

    async def on_member_join(self, member):
        if self.bleeding:
            self.log('Initiating verification procedure for user "{}".'.format(member.name))
            await self.verify(member)

    async def verify(self, member):
        msg  = 'Please send your EPITECH mail adress\n'
        msg += 'i.e.: ```yournam_e@epitech.eu```\n'
        msg += 'It has to be an EPITECH adress, any other adress will not be accepted'

        await self.send_message(member, msg)

    def is_epitech(self, txt):
        if txt[-11:] != '@epitech.eu':
            return False
        # TODO : mail username (check there are no @)
        return True

if __name__ == '__main__':
    main()
