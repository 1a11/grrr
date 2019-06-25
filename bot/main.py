import glob
import json
import time
import discord
from discord.ext import commands
from loguru import logger
import asyncio
from pathlib import Path
from cogs.utils import checks # This will say error in most IDSs, Ignore it



# initiate logger
logger.add(f"file_{str(time.strftime('%Y%m%d-%H%M%S'))}.log",
           rotation="1 day",
           enqueue=True,
           compression="zip")


def config_load():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)


async def run():
    global bot
    config = config_load()
    bot = Bot(config=config,
              description=config['description'])
    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix_,
            description=kwargs.pop('description')
        )
        self.start_time = None
        self.app_info = None
        self.loop.create_task(self.load_all_extensions())


    async def get_prefix_(self, bot, message):
        prefix = ['!']
        return commands.when_mentioned_or(*prefix)(bot, message)

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                logger.success(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                logger.error(f'failed to load extension {error}')

        try:
            self.add_cog(Maintence(bot))
            logger.success(f'loaded Maintence Cog')
        except Exception as e:
            error = f'Maintenance Cog\n {type(e).__name__} : {e}'
            logger.error(f'failed to load Maintenance Cog Something is seriously wrong! {error}')

    async def on_ready(self):
        self.app_info = await self.application_info()
        logger.info(f'Logged in as: {self.user.name}')
        logger.info(f'Using discord.py version: {discord.__version__}')
        logger.success('Bot is ready')

    async def on_message(self, message):
        if message.author.bot:
            return  # ignore all bots
        await self.process_commands(message)


class Maintence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def exit(self, ctx):
        await bot.logout()

    @commands.command(hidden=True)
    @checks.is_admin()
    async def reload(self, ctx,  cog = None):
        if cog is None:
            await ctx.send("Please specify a cog")
        else:
            try:
                bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f"```diff\n+ Reloaded {cog} successfully\n```")
                logger.success(f"{cog} reloaded by {ctx.message.author.name}")
            except Exception as e:
                error = f'{cog}\n {type(e).__name__} : {e}'
                await ctx.send(f"```diff\n- Error reloading that cog: {error}\n````")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
