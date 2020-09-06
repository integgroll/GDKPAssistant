import discord
import importlib
import discordbot.cogs.account
from loguru import logger
from dynaconf import settings as dyna_settings
from discord.ext.commands import Bot

from discordbot.gdpk_assistant import GDKPABot



logger.info("Starting GDKP Assistant")
discord_bot_handle = GDKPABot()
logger.info(discord_bot_handle.commands)
logger.info(list([cog.qualified_name for cog in discord_bot_handle.get_cog("Accounts").walk_commands()]))
discord_bot_handle.run(dyna_settings.BOT_TOKEN)
logger.info("Shutting down GDKP Assistant")

