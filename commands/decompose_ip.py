import discord
from discord.ext import commands
import ipaddress

class DecomposeIPCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="decompose_ip", description="Décompose une adresse IP.")
    async def decompose_ip(self, ctx, ip: str):
        try:
            ip_obj = ipaddress.ip_address(ip)
            binary = bin(int(ip_obj))[2:].zfill(32)
            hex_value = hex(int(ip_obj)).upper()
            await ctx.respond(f"IP : `{ip}`\nBinaire : `{binary}`\nHexadécimal : `{hex_value}`")
        except ValueError:
            await ctx.respond("Erreur : Adresse IP invalide.")

def setup(bot):
    bot.add_cog(DecomposeIPCommand(bot))
