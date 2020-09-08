import discord.ext.commands


def admin_only():
    def predicate(ctx):
        return ctx.message.author.id in (ctx.bot.record_handle.show_admin(guild_id=str(ctx.message.guild.id)) or [])

    return discord.ext.commands.check(predicate)


def power_user():
    def predicate(ctx):
        return ctx.message.author.id in (ctx.bot.record_handle.show_power_user(guild_id=str(ctx.message.guild.id)) or [])

    return discord.ext.commands.check(predicate)


def end_user():
    def predicate(ctx):
        return ctx.message.author.id in []
    return discord.ext.commands.check(predicate)