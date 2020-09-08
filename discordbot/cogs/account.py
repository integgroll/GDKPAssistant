import discord.ext.commands
import discordbot.cogs.checks

from loguru import logger


class Accounts(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.check_any(discordbot.cogs.checks.admin_only(), discordbot.cogs.checks.power_user())
    @discord.ext.commands.group(name='account', invoke_without_command=False)
    async def account(self, ctx):
        """
        Group for the Account commands Don't really want this base doing anthing
        :param ctx:
        :return:
        """
        pass

    @account.group(name='show')
    async def show(self, ctx):
        """
        Show the account details for either admins, powerusers, users, or raids
        :param ctx:
        :return:
        """
        pass

    @discord.ext.commands.check_any(discordbot.cogs.checks.admin_only())
    @show.command(name='admin', aliases=['admins'])
    async def admin(self, ctx):
        """
        Send back the information on the admins for the account
        :param ctx:
        :return:
        """
        await ctx.send(ctx.message.author, ctx.bot.record_handle.show_account(guild_id=ctx.message.guild.id)["admins"])

    @show.command(aliases=['powerusers', 'poweruser', 'power_users', 'powers'])
    async def power(self, ctx):
        """
        Send back the information on the power_users for the account
        :param ctx:
        :return:
        """
        await ctx.send(ctx.message.author,
                       ctx.bot.record_handle.show_account(guild_id=ctx.message.guild.id)["power_users"])

    @show.command(aliases=['users'])
    async def user(self, ctx):
        """
        Send back the information on the users for the account
        :param ctx:
        :return:
        """
        await ctx.send(ctx.message.author, ctx.bot.record_handle.show_account(guild_id=ctx.message.guild.id)["users"])

    @show.command(aliases=['raids'])
    async def raid(self, ctx):
        """
        Send back the information on the raids for the account
        :param ctx:
        :return:
        """
        await ctx.send(ctx.message.author, ctx.bot.record_handle.show_account(guild_id=ctx.message.guild.id)["raids"])

    @account.group(name='add')
    async def add(self, ctx):
        """
        Group for the adding commands for accounts
        :param ctx:
        :return:
        """
        pass

    @discord.ext.commands.check_any(discordbot.cogs.checks.admin_only())
    @add.command()
    async def admin(self, ctx, user: discord.User):
        """
        Adds an admin user to the account
        :param ctx:
        :param user:
        :return:
        """
        await ctx.send(f"Added {user.name} to the admins list")

    @add.command(aliases=['powerusers', 'poweruser', 'power_users', 'powers'])
    async def power(self, ctx, user: discord.User):
        """
        Adds a power user to the account
        :param ctx:
        :param user:
        :return:
        """
        pass

    @add.command(aliases=['users'])
    async def user(self, ctx, user: discord.User):
        """
        Adds a regular user to the account
        :param ctx:
        :param user:
        :return:
        """
        await ctx.send("Trying to add a user, doesn't look good")
