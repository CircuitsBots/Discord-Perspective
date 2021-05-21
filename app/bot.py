import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()


class ProfBot(commands.Bot):
    def __init__(self):
        super().__init__("p!")
        self.session: aiohttp.ClientSession = None
        self.tolerance = 0.5

    def run(self):
        token = os.getenv("TOKEN")
        return super().run(token)

    async def start(self, *args, **kwargs):
        await self.set_session()
        await super().start(*args, **kwargs)

    async def set_session(self):
        self.session = aiohttp.ClientSession()

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        params = {"comment": message.content}
        async with (
            self.session.get("http://localhost:5050/analize", params=params)
            as resp
        ):
            data = await resp.json()
            if data["toxicity"] > self.tolerance:
                return await message.delete()
        await self.process_commands(message)
