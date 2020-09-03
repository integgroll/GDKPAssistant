import discord
from loguru import logger
from dynaconf import settings

discord_client_handle = discord.Client()

@discord_client_handle.event
async def on_message(message):
    """

    :param message:
    :return:
    """
    # Prevent bot from responding to itself
    if message.author == discord_client_handle.user:
        return

    if message.content.startswith('!botstart'):
        msg = f"Hello {message.author.mention}"
        await discord_client_handle.send_message(message.channel, msg)


@discord_client_handle.event
async def on_ready():
    logger.info(f"Logged in as: {discord_client_handle.user.name} - {discord_client_handle.user.id}")
    logger.info("Get Ready to ROCK!!!")

discord_client_handle.run(settings.BOT_TOKEN)


