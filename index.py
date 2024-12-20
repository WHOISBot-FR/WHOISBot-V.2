import discord
from discord.ext import commands
import logging
import os
from colorama import Fore, Style

class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.INFO: Fore.BLUE + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        'DEFAULT': "%(asctime)s - %(levelname)s - %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logging.getLogger().handlers.clear()

logger = logging.getLogger('discord')
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

def display_startup_screen():
    logo = """
    ==========================================
    ||                                       ||
    ||          W  H  O  I  S  B  O  T       ||
    ||                                       ||
    ==========================================
    """
    print(Fore.GREEN + logo + Style.RESET_ALL)

@bot.event
async def on_ready():
    logger.info(f"Bot connecté en tant que {bot.user.name}")

if __name__ == "__main__":
    TOKEN = "votre_token_ici"
    display_startup_screen()
    bot.run(TOKEN)
