import discord
import importlib
import discordbot.cogs.account
from loguru import logger
from dynaconf import settings as dyna_settings
from discord.ext.commands import Bot


class GDKPABot(discord.ext.commands.Bot):
    def __init__(self):
        """
        Build the stack of background variables that we need to maintain the state of the bot and the service
        """
        super().__init__(
            command_prefix=("!", "$"),
            description="GDKP Assistant primarily created for guilds on Atiesh, Alliance",
            pm_help=None,
            case_insensitive=True
        )

        self.server_message_state = {}

        # Load the database that you have put files in based on the configuration files
        self.record_handle = importlib.import_module(
            f"discordbot.storage.{dyna_settings.get('STORAGE_OPTION', 'dictionary_storage')}").PythonicRecord()
        self.add_cog(discordbot.cogs.account.Accounts(self))

    async def on_ready(self):
        """
        Called when the client is done preparing the data received from Discord. Usually after login is successful
         and the :attr:`Client.guilds` and co. are filled up.

        .. warning::

        This function is not guaranteed to be the first event called.
        Likewise, this function is **not** guaranteed to only be called
        once. This library implements reconnection logic and thus will
        end up calling this event whenever a RESUME request fails.
        :return:
        """

        logger.info(f"Logged in as: {self.user.name} - {self.user.id}")
        logger.info("Get Ready to ROCK!!!")

    async def on_message(self, message):
        """
        General message handler for direct messages
        :param message:
        :return:
        """
        if message.author == self.user:
            return

        if message.content.startswith('!botstart'):
            msg = f"Hello {message.author.mention}"
            await self.send_message(message.channel, msg)

    async def on_voice_state_update(self, member, before, after):
        """
        Called when a :class:`Member` changes their :class:`VoiceState`.

        The following, but not limited to, examples illustrate when this event is called:

        - A member joins a voice channel.
        - A member leaves a voice channel.
        - A member is muted or deafened by their own accord.
        - A member is muted or deafened by a guild administrator.

        :param member: The member whose voice states changed.
        :type member: :class:`Member`
        :param before: The voice state prior to the changes.
        :type before: :class:`VoiceState`
        :param after: The voice state after to the changes.
        :type after: :class:`VoiceState`
        :return:
        """

    async def on_reaction_add(self, reaction, user):
        """
        Called when a message has a reaction added to it. Similar to :func:`on_message_edit`,
        if the message is not found in the internal message cache, then this
        event will not be called. Consider using :func:`on_raw_reaction_add` instead.

        .. note::

            To get the :class:`Message` being reacted, access it via :attr:`Reaction.message`.

        :param reaction: The current state of the reaction.
        :type reaction: :class:`Reaction`
        :param user: The user who added the reaction.
        :type user: Union[:class:`Member`, :class:`User`]
        :return:
        """


discord_bot_handle.run(dyna_settings.BOT_TOKEN)
