import asyncio
import discord
from discord.ext import commands

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel   = message.channel
        self.player    = player
        self.duration  = None
        if player.duration:
            self.duration = '{0[0]}m {0[1]}'.format(divmod(player.duration, 60))

    def embed(self):
        embed = discord.Embed(title=self.player.title)
        embed.color = discord.Colour.purple()
        if self.player.uploader is not None:
            embed.add_field(name='Uploader', value=self.player.uploader)
        if self.duration is not None:
            embed.title += ' (length: {})'.format(self.duration)
        embed.set_footer(text='Requester: {}'.format(self.requester), icon_url=self.requester.avatar_url)

        return embed

    def __str__(self):
        fmt = '**{0.title}** uploaded by *{0.uploader}*'
        if self.duration:
            fmt = fmt + ' :clock3: `{0}`'.format(self.duration)
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ', embed=self.current.embed())
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, context, *, channel : discord.Channel = None):
        """Joins a voice channel."""
        if channel is None:
            channel = context.message.author.voice_channel
            if channel is None:
                await self.bot.reply('you are not in a voice channel.\n'
                + 'Please join one first or use `join <channel name>`.')
                return False

        state = self.get_voice_state(context.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(channel)
        else:
            await state.voice.move_to(channel)
        await self.bot.ok(context)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, context, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(context.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            if not hasattr(self, 'summon'):
                return
            success = await context.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```\n{}: {}\n```'
            await self.bot.send_message(context.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(context.message, player)
            if state.is_playing():
                await self.bot.reply('you queued {}'.format(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, context, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(context.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, context):
        """Pauses the currently played song."""
        state = self.get_voice_state(context.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, context):
        """Resumes the currently played song."""
        state = self.get_voice_state(context.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, context):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = context.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, context):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(context.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = context.message.author
        if voter is state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, context):
        """Shows info about the currently played song."""

        state = self.get_voice_state(context.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))
