import discord
from discord.ext import commands
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('discord')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

@bot.event
async def on_ready():
    logger.info(f"Bot connecté en tant que {bot.user.name}")

if __name__ == "__main__":
    TOKEN = "votre_token_ici"
    bot.run(TOKEN)
