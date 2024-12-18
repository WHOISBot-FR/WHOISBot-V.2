import discord
from discord.ext import commands
import socket

class ReverseDNSCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="reverse_dns", description="Effectue un reverse DNS lookup.")
    async def reverse_dns(self, ctx, ip: str):
        try:
            host = socket.gethostbyaddr(ip)[0]
            await ctx.respond(f"IP : `{ip}`\nNom d'hôte : `{host}`")
        except socket.herror:
            await ctx.respond("Erreur : Impossible de résoudre le reverse DNS.")

def setup(bot):
    bot.add_cog(ReverseDNSCommand(bot))
