import discord.ext.commands


class Accounts(discord.ext.commands.Cog):
    def __init__(self, bot_handle):
        self.bot_handle = bot_handle

    @discord.ext.commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member
