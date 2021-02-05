from textwrap import dedent

from discord.ext.commands import Bot, Cog, Context, command


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def help(self, ctx: Context):
        await ctx.send(
            dedent(
                """\
                ─　`![level|l] [user]`
                レベル関係の情報を表示します。
                
                ─　`![ranking|r]`
                上位10名のランキングを表示します。
                
                ─　獲得経験値
                1message = 1exp です。
                
                ─　次のレベルに必要な経験値の式
                (現在のレベル ** 3) * (4 / 5) + 1
                """
            )
        )


def setup(bot: Bot):
    bot.add_cog(Help(bot))
