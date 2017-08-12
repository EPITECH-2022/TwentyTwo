import json, os.path
import discord
from discord.ext import commands

from Fun import Fun

def main():

    config_file = 'config.json'

    with open(config_file) as f:
        config = json.load(f)
    description, token = config['description'], config['token']

    client = Bot(description=description)
    client.add_cog(Fun(client))
    client.run(token)

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        ''' Rewrite the command_prefix flag to force mention '''
        super().__init__(*args, command_prefix=commands.when_mentioned, **kwargs)

if __name__ == '__main__':
    main()
