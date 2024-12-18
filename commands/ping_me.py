import discord
from discord.ext import commands

class PingMeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping_me", description="Affiche le ping du bot.")
    async def ping_me(self, ctx):
        latency = round(self.bot.latency * 1000, 2)
        await ctx.respond(f"Pong ! Latence : `{latency} ms`")

def setup(bot):
    bot.add_cog(PingMeCommand(bot))
