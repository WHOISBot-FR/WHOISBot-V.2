import discord
from discord.ext import commands
from ping3 import ping
import socket
import requests
import logging

logger = logging.getLogger('discord')

class PingIPCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping_ip", description="Ping une adresse IP ou un domaine.")
    async def ping_ip(self, ctx, target: str):
        logger.info(f"Commande utilisée: /ping_ip par {ctx.author.name} pour {target}")
        await ctx.respond(f"Ping de `{target}` en cours...")

        try:
            ip = socket.gethostbyname(target)
            response_time = ping(ip)
            success = response_time is not None

            geo_url = f"http://ip-api.com/json/{ip}"
            geo_response = requests.get(geo_url).json()

            embed = discord.Embed(
                title="Résultat du Ping",
                color=discord.Color.green() if success else discord.Color.red()
            )
            embed.add_field(name="Adresse IP", value=f"`{ip}`", inline=False)
            embed.add_field(name="Statut", value="Réponse reçue" if success else "Pas de réponse", inline=False)
            if success:
                embed.add_field(name="Temps de réponse", value=f"{response_time:.2f} ms", inline=False)
            embed.add_field(name="Pays", value=geo_response.get('country', 'N/A'), inline=False)
            await ctx.edit(content=None, embed=embed)

        except Exception as e:
            logger.error(f"Erreur: {e}")
            await ctx.respond(f"Erreur lors du ping de `{target}`.")

def setup(bot):
    bot.add_cog(PingIPCommand(bot))
