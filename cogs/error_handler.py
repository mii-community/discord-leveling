from discord.ext.commands import (
    Bot,
    CheckFailure,
    Cog,
    CommandError,
    CommandNotFound,
    Context,
)


class ErrorHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        ignore_errors = (CommandNotFound, CheckFailure)
        if isinstance(error, ignore_errors):
            return

        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))
