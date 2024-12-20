import discord
from discord.ext import commands
import ipaddress
import socket
import subprocess
import requests
import logging
import time

logger = logging.getLogger('discord')

class IPInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ip_info", description="Obtenir des informations détaillées sur une adresse IP.")
    async def ip_info_command(self, ctx, ip: str):
        logger.info(f"Commande utilisée: /ip_info par {ctx.author.name} pour l'adresse IP {ip}")
        await ctx.respond(f"Recherche des informations pour l'adresse IP `{ip}`... Cela peut prendre un moment.")

        try:
            ip_obj = ipaddress.ip_address(ip)

            ping_result = self.ping_ip(ip)

            geo_data = self.get_geo_info(ip)

            embed = discord.Embed(title=f"Informations IP pour `{ip}`", color=discord.Color.blue())
            embed.add_field(name="Adresse IP", value=f"`{ip}`", inline=True)
            embed.add_field(name="Version", value=f"`IPv{ip_obj.version}`", inline=True)
            embed.add_field(name="Masque de sous-réseau", value=f"`{ip_obj.max_prefixlen}`", inline=True)

            if ping_result:
                embed.add_field(name="Répond au ping ?", value="`Oui`", inline=True)
                embed.add_field(name="Temps de réponse (ms)", value=f"`{ping_result['time']} ms`", inline=True)
            else:
                embed.add_field(name="Répond au ping ?", value="`Non`", inline=True)

            if geo_data:
                embed.add_field(name="Localisation", value=f"`{geo_data.get('city', 'N/A')}, {geo_data.get('region', 'N/A')}, {geo_data.get('country', 'N/A')}`", inline=False)
                embed.add_field(name="Organisation (ASN)", value=f"`{geo_data.get('org', 'N/A')}`", inline=False)
                embed.add_field(name="Latitude", value=f"`{geo_data.get('latitude', 'N/A')}`", inline=True)
                embed.add_field(name="Longitude", value=f"`{geo_data.get('longitude', 'N/A')}`", inline=True)

            embed.set_footer(text="Ces informations sont fournies par notre analyseur IP.")
            await ctx.edit(content=None, embed=embed)

        except ValueError:
            await ctx.edit(content=f"L'adresse IP `{ip}` n'est pas valide.")
        except Exception as e:
            logger.error(f"Erreur lors de la commande IP_INFO: {e}")
            await ctx.edit(content=f"Une erreur s'est produite lors de la récupération des informations pour `{ip}`.")

    def ping_ip(self, ip):
        """Teste si une IP répond au ping et mesure le temps de réponse."""
        try:
            start_time = time.time()
            result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            end_time = time.time()

            if result.returncode == 0:
                return {"time": round((end_time - start_time) * 1000, 2)}
            return None
        except Exception as e:
            logger.error(f"Erreur lors du ping: {e}")
            return None

    def get_geo_info(self, ip):
        """Récupère les informations de géolocalisation et ASN via l'API ipinfo.io."""
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                location = data.get("loc", "0,0").split(",")
                return {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "org": data.get("org"),
                    "latitude": location[0] if len(location) > 1 else "N/A",
                    "longitude": location[1] if len(location) > 1 else "N/A",
                }
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données IP : {e}")
            return None

def setup(bot):
    bot.add_cog(IPInfoCommand(bot))
