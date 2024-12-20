import discord
from discord.ext import commands
import whois
import logging

logger = logging.getLogger('discord')

class WhoisCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="whois", description="Obtenir des informations WHOIS pour un domaine.")
    async def whois_command(self, ctx, domain: str):
        logger.info(f"Commande utilisée: /whois par {ctx.author.name} pour le domaine {domain}")
        await ctx.respond(f"Recherche des informations WHOIS pour `{domain}`... Cela peut prendre un moment.")
        try:
            w = whois.whois(domain)
            embed = discord.Embed(title=f"Informations WHOIS pour `{domain}`", color=discord.Color.blue())

            embed.add_field(name="Domaine", value=f"`{w.domain_name}`" if w.domain_name else "`N/A`", inline=False)
            embed.add_field(name="Registrar", value=f"`{w.registrar}`" if w.registrar else "`N/A`", inline=False)
            embed.add_field(name="Statut du domaine", value=f"`{'`, `'.join(w.status)}`" if w.status else "`N/A`", inline=False)
            embed.add_field(name="Date de création", value=f"`{w.creation_date}`" if w.creation_date else "`N/A`", inline=False)
            embed.add_field(name="Date d'expiration", value=f"`{w.expiration_date}`" if w.expiration_date else "`N/A`", inline=False)
            embed.add_field(name="Date de mise à jour", value=f"`{w.updated_date}`" if w.updated_date else "`N/A`", inline=False)

            embed.add_field(name="Serveurs de noms", value=f"`{'`, `'.join(w.name_servers)}`" if w.name_servers else "`N/A`", inline=False)

            if hasattr(w, 'emails') and w.emails:
                emails = w.emails if isinstance(w.emails, list) else [w.emails]
                embed.add_field(name="Emails associés", value=f"`{'`, `'.join(emails)}`", inline=False)

            embed.add_field(name="Organisation", value=f"`{w.org}`" if w.org else "`N/A`", inline=False)
            embed.add_field(name="Pays", value=f"`{w.country}`" if w.country else "`N/A`", inline=False)
            embed.add_field(name="Ville", value=f"`{w.city}`" if w.city else "`N/A`", inline=False)
            embed.add_field(name="Adresse", value=f"`{w.address}`" if w.address else "`N/A`", inline=False)

            embed.set_footer(text="Ces informations sont fournies par notre prestataire.")
            await ctx.edit(content=None, embed=embed)

        except Exception as e:
            logger.error(f"Erreur lors de la commande WHOIS: {e}")
            await ctx.edit(content=f"Une erreur s'est produite lors de la récupération des informations WHOIS pour `{domain}`.")

def setup(bot):
    bot.add_cog(WhoisCommand(bot))
