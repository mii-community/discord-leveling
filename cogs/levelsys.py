import asyncio
import json
from textwrap import dedent

import const
from discord import Embed, Member, Message
from discord.ext.commands import Bot, Cog, Context, command


class LevelSys(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.loop.create_task(self.save_leveling_data())
        with open("leveling.json") as f:
            self.leveling = json.load(f)

    async def save_leveling_data(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open("leveling.json", "w") as f:
                json.dump(self.leveling, f, indent=4)
            await asyncio.sleep(5)

    def level_up_exp(self, current_level: int):
        return round((current_level ** 3) * (4 / 5) + 1)

    def level_up(self, user_id: str):
        current_exp = self.leveling[user_id]["exp"]
        current_level = self.leveling[user_id]["level"]
        if current_exp >= self.level_up_exp(current_level) or current_level == 0:
            self.leveling[user_id]["level"] += 1
            return True
        else:
            return False

    @Cog.listener()
    async def on_message(self, message: Message):
        author = message.author
        if author.bot:
            return

        user_id = str(author.id)
        if user_id not in self.leveling:
            self.leveling[user_id] = {}
            self.leveling[user_id]["exp"] = 0
            self.leveling[user_id]["level"] = 0
        self.leveling[user_id]["exp"] += 1
        if not self.level_up(user_id):
            return
        current_level = self.leveling[user_id]["level"]
        current_exp = self.leveling[user_id]["exp"]
        embed = Embed(
            title="Level UP!",
            description=dedent(
                f"""\
                {author.mention} のレベルが **{current_level}** に上がりました。
                次のレベルアップに必要な経験値は **{self.level_up_exp(current_level) - current_exp}** です。
                """
            ),
            timestamp=message.created_at,
        )
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"#{message.channel.name}")
        await self.bot.get_channel(const.CH_LEVELUP_LOG).send(embed=embed)

    @command(aliases=["l"])
    async def level(self, ctx: Context, user: Member = None):
        if user is None:
            user = ctx.author
        user_id = str(user.id)
        try:
            current_level = self.leveling[user_id]["level"]
            current_exp = self.leveling[user_id]["exp"]
        except KeyError:
            await ctx.send("そのユーザーはまだレベルがありません。")
            return
        rankings = sorted(
            self.leveling.items(), key=lambda x: x[1]["exp"], reverse=True
        )
        rank = 1
        for x in rankings:
            if user.id == int(x[0]):
                break
            rank += 1
        level_up_exp = self.level_up_exp(current_level)
        progress = round((current_exp / level_up_exp) * 10)
        progress_detail = round((current_exp / level_up_exp) * 100)
        progress_bar = f"{'<:i:807039019590352906>' * progress + '<:i:807039030461595710>' * (10 - progress)}"
        embed = Embed(
            title="Level Information",
            description=dedent(
                f"""\
                {user.mention} **Lv.{current_level} Rank.{rank}**
                累計経験値　⏩　**{current_exp}**
                次のレベルアップまで　⏩　**{level_up_exp - current_exp}**
                進捗: **{progress_detail}%**
                {progress_bar}
                """
            ),
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @command(aliases=["r"])
    async def ranking(self, ctx: Context):
        i = 1
        rankings = sorted(
            self.leveling.items(), key=lambda x: x[1]["exp"], reverse=True
        )
        content = ""
        for data in rankings:
            try:
                user = ctx.guild.get_member(int(data[0]))
                exp = data[1]["exp"]
                level = data[1]["level"]
                content += f"{i}位: {user.mention} **Lv.{level}**\n累計経験値: **{exp}**\n\n"
                i += 1
            except Exception:
                pass
            if i == 11:
                break
        embed = Embed(
            title="みぃレベルランキング",
            description=content,
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/752286472383758416/807025755992490046/b93db8f468cc5f8b533b3d6c1dba1267.png"
        )
        embed.set_footer(text="上位10名のみが掲載されます。")
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(LevelSys(bot))
