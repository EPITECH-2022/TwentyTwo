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
        from datetime    import datetime
        if member is None:
            member = context.message.author
        msg = '`{}` joined Discord on {}'
        await self.bot.say(msg.format(member, datetime.strftime(member.created_at, '%d %B %Y at %X')))
        await self.bot.replied(context)

    @commands.command(pass_context=True)
    async def joined(self, context, member: discord.Member = None):
        ''' Tells the age of a member on this Discord server '''
        from datetime    import datetime
        if member is None:
            member = context.message.author
        msg = '`{}` joined *{}* on {}'
        await self.bot.say(msg.format(member, member.server, datetime.strftime(member.joined_at, '%d %B %Y at %X')))
        await self.bot.replied(context)

    '''
    @commands.command(name='help')
    async def _help(self):
        await self.bot.reply('ask `Tina#4153`')
    '''

    @commands.command(pass_context=True, aliases=['ri', 'riz', 'regional_indicator', 'bi'])
    async def emoji(self, context):
        ''' Sends a text and replace letters with regional indicators '''
        from unidecode   import unidecode
        content = self.bot.get_text(context)
        if content in [None, '', ' '] or context.invoked_with == 'riz' and not self.bot.is_owner(context.message.author):
            return
        msg = ''
        if context.invoked_with == 'ri':
            msg += '`{}`: '.format(context.message.author)
        for c in content:
            if c.isalpha():
                b = invoked_with == 'bi' and c in ['b', 'B', 'p', 'P']
                if b:
                    msg += ':b:'
                else:
                    msg += ':regional_indicator_{}:'.format(unidecode(c.lower()))
            else:
                msg += c
        await self.bot.say(msg)
        await self.bot.replied(context)
        if context.invoked_with in ['ri', 'riz']:
            try:
                await self.bot.delete_message(context.message)
            except discord.errors.Forbidden:
                pass

    @commands.command(pass_context=True)
    async def decode(self, context):
        ''' Convert any character to its ASCII counterpart '''
        from unidecode   import unidecode
        content = self.bot.get_text(context)
        if content in [None, ' ']:
            await self.bot.doubt(context)
            return
        msg = unidecode(content)
        if msg is None:
            await self.bot.doubt(context)
            return
        await self.bot.say(msg)
        await self.bot.replied(context)

    @commands.command(pass_context=True, aliases=['prononciation', 'pron'])
    async def pronunciation(self, context):
        ''' Uses Google API to fetch the pronunciation of a word (useful for Japanese, Korean, etc) '''
        content       = self.bot.get_text(context)
        from googletrans import Translator
        translator    = Translator()
        language      = translator.detect(content).lang[:2]
        pronunciation = translator.translate(content, dest=language).pronunciation
        if pronunciation is None:
            msg  = 'No specific pronunciation found for this text.\n'
            msg += 'Detected language : {}'.format(language)
            await self.bot.reply(msg)
            await self.bot.replied(context)
        else:
            embed = discord.Embed(colour=discord.Colour.dark_blue())
            embed.add_field(name='Pronunciation', value=pronunciation)
            embed.set_footer(text=language)
            await self.bot.say(embed=embed)
            await self.bot.replied(context)

    @commands.command(pass_context=True, aliases=['trad', 'trans', 'traduit'])
    async def translate(self, context):
        ''' Translates a text to a destination language '''
        content       = self.bot.get_text(context)
        from googletrans import Translator
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
            await self.bot.replied(context)
        except ValueError as e:
            await self.bot.report(context, e)

    @commands.command(pass_context=True, aliases=['wiki'])
    async def wikipedia(self, context, lang: str = None, query: str = None):
        ''' Get a page from wikipedia and reply with an embed '''
        query = self.bot.get_text(context)
        if lang is not None:
            if lang.startswith('(') and lang.endswith(')'):
                query = query[len(lang) + 1:]
                lang = lang[1:-1]
            else:
                lang = None
        if query in [None, '', ' ']:
            await self.bot.doubt(context)
            return
        try:
            import wikipedia
            if lang is not None and lang in wikipedia.languages().keys():
                wikipedia.set_lang(lang)
            else:
                wikipedia.set_lang('en')
            page    = wikipedia.page(query)
            summary = page.summary
            if len(summary) > 1222: # totally arbitrary chosen number
                summary = summary[:1220] + '...'
            embed   = discord.Embed(title=page.title, description=summary, url=page.url)
            embed.set_footer(text=page.url)
            if self.bot.config['bleeding']:
                if len(page.images) > 0:
                    embed.set_image(url=page.images[0])
            await self.bot.say(embed=embed)
            await self.bot.replied(context)
        except wikipedia.PageError as e:
            await self.bot.reply('{}\nMake sure you search for page titles in the language that you have set.'.format(e))
            await self.bot.doubt(context)
        except KeyError:
            pass
        except wikipedia.DisambiguationError as e:
            msg = '```\n{}\n```'.format(e)
            await self.bot.doubt(context)
            await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def toascii(self, context):
        text = self.bot.get_text(context)
        msg = ''
        for c in text:
            msg += str(ord(c)) + ' '
        await self.bot.reply(msg)
        await self.bot.replied(context)

    @commands.command(pass_context=True)
    async def fromascii(self, context):
        text = self.bot.get_text(context)
        msg = ''
        try:
            for code in text.split():
                code = int(code)
                msg += chr(code)
            await self.bot.reply(msg)
            await self.bot.replied(context)
        except e:
            msg = '```\n{}\n```'.format(e)
            await self.doubt(context)
            await self.bot.say(msg)
