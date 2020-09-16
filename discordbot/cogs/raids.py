import datetime

import discord.ext.commands
import discordbot.cogs.checks
import discordbot.tools.embed
import discordbot.tools.ratings

from loguru import logger


class Raids(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.character_class_spec_list = {"druid": ["melee", "ranged", "heals", "tank"],
                                          "hunter": ["ranged"],
                                          "mage": ["ranged"],
                                          "paladin": ["resto"],
                                          "priest": ["resto"],
                                          "rogue": ["melee"],
                                          "shaman": ["lol"],
                                          "warlock": ["ranged"],
                                          "warrior": ["tank", "melee"]}

    @discord.ext.commands.check_any(discordbot.cogs.checks.admin_only(), discordbot.cogs.checks.power_user())
    @discord.ext.commands.group(name='raids', aliases=['raid'], invoke_without_command=False)
    async def raids(self, ctx):
        """
        Base command group for an end user account to manage their characters
        :param ctx:
        :return:
        """
        pass

    @discord.ext.commands.check_any(discordbot.cogs.checks.admin_only(), discordbot.cogs.checks.power_user())
    @raids.command(name='add')
    async def add(self, ctx, raid_instance: str, start_datetime: str):
        """
        Base raid command to add a new raid to the channel that you are current in
        :param ctx:
        :param raid_instance:
        :param start_datetime:
        :return:
        """
        valid_datetime = None
        valid_raid = None
        current_raids = ["AQ-40", "BWL", "Naxx"]
        if raid_instance not in current_raids:
            await ctx.message.author.send(f"The raid needs to be one of: {current_raids}")
        else:
            valid_raid = raid_instance
        try:
            # Just checking to see that the datetime actually functions
            datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
            valid_datetime = start_datetime
        except Exception as error_handle:
            await ctx.message.author.send(f"The datetime needs to be in the format of YY-MM-DD HH/MM/SS")

        if valid_datetime and valid_raid:
            raid_message = await ctx.message.channel.send("New Raid being created please wait a moment...")

            raid_id = self.bot.record_handle.add_raid(guild_id=raid_message.guild.id, raid_instance=raid_instance,
                                                      start_datetime=start_datetime, raid_message_id=raid_message.id)

            embed_handle = discordbot.tools.embed.generate_embed(raid_id=raid_id, raid_instance=raid_instance,
                                                                 start_datetime=start_datetime, signups=[])

            await raid_message.edit(content=None, embed=embed_handle)

            for reaction in await ctx.guild.fetch_emojis():
                if reaction.name in self.bot.reaction_list:
                    await raid_message.add_reaction(reaction)
