import discord
import importlib
import discordbot.cogs.account
import discordbot.cogs.character
import discordbot.cogs.raids
import discordbot.tools.ratings
from loguru import logger
from dynaconf import settings as dyna_settings
import discord.ext.commands


class GDKPABot(discord.ext.commands.Bot):
    def __init__(self):
        """
        Build the stack of background variables that we need to maintain the state of the bot and the service
        """
        super().__init__(
            command_prefix="!",
            description="GDKP Assistant primarily created for guilds on Atiesh, Alliance",
            pm_help=None,
            case_insensitive=True
        )

        self.add_cog(discordbot.cogs.account.Accounts(self))
        self.add_cog(discordbot.cogs.character.Characters(self))
        self.add_cog(discordbot.cogs.raids.Raids(self))

        self.ratings_handle = discordbot.tools.ratings.CharacterRater()

        self.reaction_list = ["HealsDruid", "HealsPaladin", "HealsPriest", "TankWarrior", "TankDruid",
                              "MeleeDruid", "MeleeRogue", "MeleeWarrior", "RangedHunter", "RangedWarlock",
                              "RangedMage"]

        self.server_message_state = {}
        # guild:{user_id:{message_state,past_info}}

        # Load the database that you have put files in based on the configuration files
        self.record_handle = importlib.import_module(
            f"discordbot.storage.{dyna_settings.get('STORAGE_OPTION', 'dictionary_storage')}").PythonicRecord()

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
            await message.channel.send(f"Hello {message.author.mention}")
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        """
        Manage the errors that are found in the bot during execution
        :param ctx:
        :param error:
        :return:
        """
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.channel.send(
                f"Seriously {ctx.message.author.id}, you don't have the rights for that command")

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

    async def on_raw_reaction_add(self, reaction, user):
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
        if reaction.name not in self.reaction_list:
            await reaction.clear()
        else:
            raid_handle = self.record_handle.get_raid_by_message_id(reaction.message.guild.id, reaction.message.id)

    async def on_guild_join(self, guild):
        """
        Called when a guild adds this bot, or when the bot creates a guild, but let's not do that part okay
        :param guild:
        :return:
        """
        logger.info(f"Joined {guild}")
        if guild.id not in self.record_handle.list_accounts():
            self.record_handle.add_account(guild.id, self.owner_id)

    async def user_communication_state(self, ctx):
        """
        process a message's user's command state
        :param ctx:
        :return:
        """

        user = ctx.message.author
        guild = ctx.message.guild

        user_state = self.record_handle.get_user_state(guild.id, user.id)
        if user_state == None and not self.record_handle.show_user(guild.id, user.id):
            # This is the default state, Create a user here.
            self.record_handle.add_user(guild.id, user.id)
            self.record_handle.set_user_state(guild.id, user.id, "2")
            user_state = "2"
            await ctx.send(ctx.message.author, "We have never seen your user before, so we added you.")
        if user_state == "2":
            # Present the character selection list
            characters = self.record_handle.show_user(guild.id, user.id).get("characters", [])
            character_option_index = 0
            character_values = []
            for character in characters:
                character_option_index += 1
                character_values.append(
                    f"{character_option_index}: {character['name']} the {character['spec']} {character['class']}")
            character_values.append(f"{character_option_index+1}: New Character")
            ctx.send(ctx.message.author,"\n".join(character_values))
            self.record_handle.set_user_state(guild.id, user.id, "3")
        if user_state == "3":
            characters = self.record_handle.show_user(guild.id, user.id).get("characters", [])
            if str(ctx.message.content).isnumeric():
                character_selection = int(ctx.message.content) - 1
                if character_selection < len(characters):
                    # Selected Character
                     # need to consider for an update of a character instead of just signing up current ones
                     # This will need a different state machine item
                    self.record_handle.set_user_state(guild.id, user.id, "5")
                elif character_selection == len(characters):
                    # Adding a new Character
                    pass

"""
State Machine Order:
1: Create User if does not exist
2: Present User with character selection
3: - Present User with character creation if selected - add new character to raid
4: - Add character to the raid
5: Query User for bids on items until they stop
"""
