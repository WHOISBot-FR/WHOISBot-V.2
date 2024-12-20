import discord
from discord.ext import commands
import ssl
import socket
import logging
from datetime import datetime

logger = logging.getLogger('discord')

class SSLInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ssl_info", description="Obtenir des informations sur le certificat SSL d'un site.")
    async def ssl_info_command(self, ctx, url: str):
        logger.info(f"Commande utilisée: /ssl_info par {ctx.author.name} pour l'URL {url}")
        await ctx.respond(f"Analyse des informations SSL pour `{url}`...")

        if not url.startswith("http"):
            url = f"https://{url}"
        host = url.split("//")[-1].split("/")[0]

        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()

            issuer = dict(x[0] for x in cert.get("issuer", []))
            subject = dict(x[0] for x in cert.get("subject", []))
            valid_from = datetime.strptime(cert.get("notBefore"), "%b %d %H:%M:%S %Y %Z")
            valid_to = datetime.strptime(cert.get("notAfter"), "%b %d %H:%M:%S %Y %Z")
            
            san_entries = cert.get("subjectAltName", [])
            san = ", ".join(entry[1] for entry in san_entries if entry[0] == "DNS")

            embed = discord.Embed(title=f"Informations SSL pour `{host}`", color=discord.Color.green())
            embed.add_field(name="Émetteur (Issuer)", value=f"`{issuer.get('organizationName', 'N/A')}`", inline=False)
            embed.add_field(name="Propriétaire (Subject)", value=f"`{subject.get('commonName', 'N/A')}`", inline=False)
            embed.add_field(name="Valide depuis", value=f"`{valid_from.strftime('%Y-%m-%d %H:%M:%S')}`", inline=True)
            embed.add_field(name="Expire le", value=f"`{valid_to.strftime('%Y-%m-%d %H:%M:%S')}`", inline=True)
            embed.add_field(name="Domaines alternatifs (SAN)", value=f"`{san}`" if san else "`N/A`", inline=False)
            embed.set_footer(text="Ces informations sont fournies par notre analyseur SSL.")

            await ctx.edit(content=None, embed=embed)

        except Exception as e:
            logger.error(f"Erreur lors de la commande SSL_INFO: {e}")
            await ctx.edit(content=f"Une erreur s'est produite lors de l'analyse du certificat SSL pour `{url}`.")

def setup(bot):
    bot.add_cog(SSLInfoCommand(bot))
