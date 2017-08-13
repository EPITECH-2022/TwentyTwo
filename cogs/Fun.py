from unidecode import unidecode
from datetime import datetime

import discord
from discord.ext import commands

class Fun:
    '''
    A collection of commands to rolls dices, send cats, and drop mixtapes (probably)
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self):
        ''' says the robot '''
        await self.bot.reply('hi!')

    @commands.command()
    async def hi(self):
        ''' says the IA '''
        await self.bot.reply('hello!')

    @commands.command(pass_context=True)
    async def age(self, context, member: discord.Member = None):
        ''' Tells the age of a Discord account '''
        if member is None:
            member = context.message.author
        msg = '`{}` joined Discord on {}'
        await self.bot.say(msg.format(member, datetime.strftime(member.created_at, '%d %B %Y at %X')))

    @commands.command(pass_context=True)
    async def joined(self, context, member: discord.Member = None):
        ''' Tells the age of a Discord account '''
        if member is None:
            member = context.message.author
        msg = '`{}` joined *{}* on {}'
        await self.bot.say(msg.format(member, member.server, datetime.strftime(member.joined_at, '%d %B %Y at %X')))

    @commands.command(name='help')
    async def _help(self):
        await self.bot.reply('ask `Tina#4153`')

    @commands.command(pass_context=True, aliases=['ri', 'riz', 'regional_indicator'])
    async def emoji(self, context):
        content = context.message.content[(len(context.prefix + context.invoked_with)) + 1:]
        if content in [None, '', ' '] or context.invoked_with == 'riz' and not self.bot.is_owner(context.message.author):
            return
        msg = ''
        if context.invoked_with == 'ri':
            msg += '`{}`: '.format(context.message.author)
        for c in unidecode(content):
            if c.isalpha():
                msg += ':regional_indicator_{}:'.format(c.lower())
            else:
                msg += c
        await self.bot.say(msg)
        if context.invoked_with in ['ri', 'riz']:
            try:
                await self.bot.delete_message(context.message)
            except discord.errors.Forbidden:
                pass

    @commands.command(pass_context=True)
    async def decode(self, context):
        content = context.message.content[(len(context.prefix + context.invoked_with)) + 1:]
        if content in [None, ' ']:
            return
        await self.bot.say(unidecode(content))
