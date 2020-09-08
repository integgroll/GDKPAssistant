import discord.ext.commands
import discordbot.cogs.checks

from loguru import logger


class Characters(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.character_class_spec_list = {"druid": ["melee", "ranged", "heals"],
                                          "hunter": ["ranged"],
                                          "mage": ["ranged"],
                                          "paladin": ["resto"],
                                          "priest": ["resto"],
                                          "rogue": ["melee"],
                                          "shaman": ["lol"],
                                          "warlock": ["ranged"],
                                          "warrior": ["tank", "melee"]}

    @discord.ext.commands.group(name='character', invoke_without_command=False)
    async def character(self, ctx):
        """
        Base command group for an end user account to manage their characters
        :param ctx:
        :return:
        """
        pass

    @character.command(name="list", aliases=['show'])
    async def list(self, ctx):
        """
        list all of the characters in a users account
        :param ctx:
        :return:
        """

        user_handle = ctx.bot.record_handle.show_user(ctx.guild.id, ctx.message.author.id)
        logger.info(user_handle)
        if user_handle:
            await ctx.message.channel.send(user_handle["characters"])
        else:
            await ctx.message.channel.send(f"No characters found for {ctx.message.author.nick}")

    @character.command(name="add", aliases=['update'])
    async def add(self, ctx, character_name, character_class, character_spec):
        """
        Add a character to the provided account
        :param ctx:
        :return:
        """
        logger.info("Attempting to add/update a character in your account")
        if character_class in self.character_class_spec_list:
            logger.info(character_class)
            if character_spec in self.character_class_spec_list[character_class]:
                logger.info(character_spec)
                if ctx.message.author.id not in self.bot.record_handle.list_user(ctx.guild.id):
                    logger.info("user not found, creating user")
                    ctx.bot.record_handle.add_user(ctx.guild.id, ctx.message.author.id)
                logger.info(ctx.bot.record_handle.list_user(ctx.guild.id))
                user_object = ctx.bot.record_handle.get_user(ctx.message.author.id)
                logger.info(user_object)
                matching_character = [character for character in user_object["characters"] if
                                      character["name"] == character_name and character["class"] == character_class and
                                      character["spec"] == character_spec]
                logger.info(matching_character)
                if matching_character:
                    logger.info("Found a matching character, have to delete it first")
                    ctx.bot.record_handle.delete_character_from_user(ctx.guild.id, ctx.message.author.id,
                                                                     character_name, character_class, character_spec)
                logger.info("Starting collection of ratings")
                character_ratings = ctx.bot.ratings_handle.get_character_ratings(character_name, character_spec)
                logger.info(character_ratings)
                ctx.bot.record_handle.add_character_to_user(ctx.guild.id, ctx.message.author.id, character_name,
                                                            character_class, character_spec, character_ratings)
                await ctx.message.channel.send(
                    f"Set {character_name} the {character_spec} {character_class} with scores of {character_ratings}")
            else:
                await ctx.message.channel.send(
                    f"Spec for {character_class} must be one of: {self.character_class_spec_list[character_class]}")
        else:
            await ctx.message.channel.send(f"Class must be one of: {self.character_class_spec_list.keys()}")
