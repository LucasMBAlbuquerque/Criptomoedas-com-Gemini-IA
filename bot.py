import asyncio
from decouple import config
import discord
from discord.ext import commands
import nest_asyncio
from decouple import config

intents = discord.Intents.all()

nest_asyncio.apply()
bot = commands.Bot('!', intents=intents)

async def carregar_cogs(bot):
    await bot.load_extension("criptoprecos.cripto")
    await bot.load_extension("respostas")

TOKEN_DISC = config("TOKEN_DISC")
async def main():
    async with bot:
        await carregar_cogs(bot)
        await bot.start(TOKEN_DISC)

asyncio.run(main())
