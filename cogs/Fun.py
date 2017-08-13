from unidecode   import unidecode
from datetime    import datetime
from googletrans import Translator
import googletrans.constants

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

    '''
    @commands.command(name='help')
    async def _help(self):
        await self.bot.reply('ask `Tina#4153`')
    '''

    @commands.command(pass_context=True, aliases=['ri', 'riz', 'regional_indicator'])
    async def emoji(self, context):
        ''' Sends a text and replace letters with regional indicators '''
        content = self.bot.get_text(context)
        if content in [None, '', ' '] or context.invoked_with == 'riz' and not self.bot.is_owner(context.message.author):
            return
        msg = ''
        if context.invoked_with == 'ri':
            msg += '`{}`: '.format(context.message.author)
        for c in content:
            if c.isalpha():
                msg += ':regional_indicator_{}:'.format(unidecode(c.lower()))
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
        ''' Convert any character to its ASCII counterpart '''
        content = self.bot.get_text(context)
        if content in [None, ' ']:
            return
        msg = unidecode(content)
        if msg is None:
            return
        await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['prononciation', 'pron'])
    async def pronunciation(self, context):
        ''' Uses Google API to fetch the pronunciation of a word (useful for Japanese, Korean, etc) '''
        content       = self.bot.get_text(context)
        translator    = Translator()
        language      = translator.detect(content).lang[:2]
        pronunciation = translator.translate(content, dest=language).pronunciation
        if pronunciation is None:
            msg  = 'No specific pronunciation found for this text.\n'
            msg += 'Detected language : {}'.format(language)
            await self.bot.reply(msg)
        else:
            embed = discord.Embed(colour=discord.Colour.dark_blue())
            embed.add_field(name='Pronunciation', value=pronunciation)
            embed.set_footer(text=language)
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, aliases=['trad', 'trans', 'traduit'])
    async def translate(self, context):
        ''' Translates a text to a destination language '''
        content       = self.bot.get_text(context)
        translator    = Translator()
        language      = content[:2]
        content       = content[3:]
        try:
            translated    = translator.translate(content, dest=language)
            embed = discord.Embed(colour=discord.Colour.dark_blue())
            embed.add_field(name='Translation', value=translated.text)
            embed.set_footer(text='{} -> {}'.format(translated.src, translated.dest))
            pronunciation = translator.translate(translated.text, dest=language).pronunciation
            if pronunciation != None and pronunciation != translated.text:
                embed.add_field(name='Pronunciation', value=pronunciation)
            await self.bot.say(embed=embed)
        except ValueError as e:
            await self.bot.report(context, e)
