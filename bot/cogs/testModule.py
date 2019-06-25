from discord.ext import commands
import discord
import re
from loguru import logger
from .utils import checks # This will say error in most IDSs, Ignore it



class CommonSpam(commands.Cog):
    """
    Fights against common spam that can plague discord servers
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def countEmojis(self, message: discord.Message):
        count = len(re.findall("(\:[a-z_1-9A-Z]+\:)", message.content)) # custom emojis
        if count == 0: # Test for Unicode Emojis
            count = len(re.findall('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|'
                                   '\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])', message.content))
        return count

    @commands.Cog.listener()
    async def on_message(self, message):
        number_of_emojis = await self.countEmojis(message)
        if number_of_emojis >= 3:
            await message.delete()
            channel = await message.author.create_dm()
            await channel.send("Please do not spam")
        await self.bot.process_commands(message)

    @commands.command()
    @checks.is_admin()
    async def commonspam(self, ctx, setting = None):
        """
        Turn on or off the command spam checks
        :param ctx:
        :param setting: on or off
        :return:
        """
        if setting is None:
            await ctx.send("Please specify a setting! (on | off)")
        else:
            if setting.lower() == "on" or setting.lower() == "off":
                pass
            else:
                await ctx.send("Please specify a *correct* setting! (on | off)")




def setup(bot):
    bot.add_cog(CommonSpam(bot))
