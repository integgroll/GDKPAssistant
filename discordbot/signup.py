import discord
from loguru import logger
from dynaconf import settings

from discord.ext.commands import Bot

discord_bot_handle = Bot(command_prefix=("!","$"))


class GDKPABot(discord.ext.commands.Bot):
    def __init__(self):
        """

        """


@discord_bot_handle.event
async def on_message(message):
    """

    :param message:
    :return:
    """
    # Prevent bot from responding to itself
    if message.author == discord_bot_handle.user:
        return

    if message.content.startswith('!botstart'):
        msg = f"Hello {message.author.mention}"
        await discord_bot_handle.send_message(message.channel, msg)


@discord_bot_handle.event
async def on_ready():
    logger.info(f"Logged in as: {discord_bot_handle.user.name} - {discord_bot_handle.user.id}")
    logger.info("Get Ready to ROCK!!!")

@discord_bot_handle.message
async def on_reaction_add(reaction, user):
    """
    When a reaction is added see if the message corresponds to one of the ones we are tracking and
    if so then find the user attached there and vet them, then add that data somewhere?
    :param reaction:
    :param user:
    :return:
    """

@discord_bot_handle.message
async def on_reaction_remove(reaction, user):
    """

    :param reaction:
    :param user:
    :return:
    """



@discord_bot_handle.command(name='fuckyeah',
                description="Test command that is just fuck yeah",
                brief="Fuck Yeah",
                aliases=['fy', 'fhy'],
                pass_context=True)
async def fuckyar(context):
    """
    This is a comment for the arbitrary fuck yeah command
    :param context:
    :return:
    """
    async with context.with_typing():
        await context.send("Fuck Yeah!")


discord_bot_handle.run(settings.BOT_TOKEN)


