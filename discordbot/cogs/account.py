import discord.ext.commands


class Accounts(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.group(name='account', invoke_without_command=False)
    async def account(self, ctx):
        """
        Group for the Account commands Don't really want this base doing anthing
        :param ctx:
        :param account_name:
        :return:
        """
        pass

    @account.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @account.group(name='show')
    async def show(self, ctx):
        """
        Show the account details for either admins, powerusers, users, or raids
        :param ctx:
        :param subcommand:
        :return:
        """
        await ctx.send("This is a test of the show group to check for permissions here")

    @show.command()
    async def admin(self, ctx):
        """
        Send back the information on the admins for the account
        :param ctx:
        :return:
        """
        if ctx.message.author in ctx.bot.record_handle.show_admin_account(account_number=ctx.message.server):
            await ctx.send(ctx.message.author,
                                       ctx.bot.record_handle.show_account(account_number=ctx.message.server)["admins"])
        else:
            await ctx.send("Permission Denied, not in admins list")

    @show.command(aliases=['powerusers', 'poweruser', 'power_users', 'powers'])
    async def power(self, ctx):
        """
        Send back the information on the power_users for the account
        :param ctx:
        :return:
        """
        if ctx.message.author in ctx.bot.record_handle.show_admin_account(account_number=ctx.message.server):
            await ctx.send(ctx.message.author,
                                       ctx.bot.record_handle.show_account(account_number=ctx.message.server)[
                                           "power_users"])
        else:
            await ctx.send("Permission Denied, not in admins list")

    @show.command(aliases=['users'])
    async def user(self, ctx):
        """
        Send back the information on the users for the account
        :param ctx:
        :return:
        """
        if ctx.message.author in ctx.bot.record_handle.show_admin_account(account_number=ctx.message.server):
            await ctx.send(ctx.message.author,
                                       ctx.bot.record_handle.show_account(account_number=ctx.message.server)["users"])
        else:
            await ctx.send("Permission Denied, not in admins list")

    @show.command(aliases=['raids'])
    async def raid(self, ctx):
        """
        Send back the information on the raids for the account
        :param ctx:
        :return:
        """
        if ctx.message.author in ctx.bot.record_handle.show_admin_account(account_number=ctx.message.server):
            await ctx.send(ctx.message.author,
                                       ctx.bot.record_handle.show_account(account_number=ctx.message.server)["raids"])
        else:
            await ctx.send("Permission Denied, not in admins list")

    @account.group(name='add')
    async def add(self, ctx):
        """
        Group for the adding commands for accounts
        :param ctx:
        :return:
        """
        await ctx.send("This is a test of the show group to check for permissions here")

    @add.command()
    async def admin(self, ctx, user_name: str):
        """
        Adds an admin user to the account
        :param ctx:
        :param user_name:
        :return:
        """
        pass

    @add.command(aliases=['powerusers', 'poweruser', 'power_users', 'powers'])
    async def power(self, ctx, user_name: str):
        """
        Adds a power user to the account
        :param ctx:
        :param user_name:
        :return:
        """
        pass

    @add.command(aliases=['users'])
    async def user(self, ctx, user_name: str):
        """
        Adds a regular user to the account
        :param ctx:
        :param user_name:
        :return:
        """
        await ctx.send("Trying to add a user, doesn't look good")
