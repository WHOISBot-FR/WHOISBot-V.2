import discord
from discord.ext import commands
import psutil

class ServerStatsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="server_stats", description="Affiche l'utilisation du serveur.")
    async def server_stats(self, ctx):
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        await ctx.respond(f"CPU : `{cpu_percent}%`\nRAM : `{mem.percent}%` utilisée")

def setup(bot):
    bot.add_cog(ServerStatsCommand(bot))
