import io, json, os.path
import discord
from discord.ext import commands

from pprint import pprint

def main():

    config_file = 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    description, token = config['description'], config['token']

    client = Bot(description=description)
    client.run(token)

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=commands.when_mentioned, **kwargs)


if __name__ == '__main__':
    main()
