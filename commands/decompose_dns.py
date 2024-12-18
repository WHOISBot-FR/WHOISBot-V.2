import discord
from discord.ext import commands
import dns.resolver

class DecomposeDNSCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="decompose_dns", description="Décompose les enregistrements DNS d'un domaine.")
    async def decompose_dns(self, ctx, domain: str):
        await ctx.respond(f"Recherche des enregistrements DNS pour `{domain}`...")
        try:
            resolver = dns.resolver.Resolver()
            records = ["A", "MX", "NS", "CNAME", "TXT"]
            results = {}
            for record in records:
                try:
                    answers = resolver.resolve(domain, record)
                    results[record] = [str(answer) for answer in answers]
                except dns.resolver.NoAnswer:
                    results[record] = []

            embed = discord.Embed(title="Enregistrements DNS", color=discord.Color.blue())
            for record, values in results.items():
                value = "\n".join(values) if values else "Aucun enregistrement trouvé."
                embed.add_field(name=record, value=value, inline=False)

            await ctx.edit(content=None, embed=embed)
        except Exception as e:
            await ctx.respond(f"Erreur : {str(e)}")

def setup(bot):
    bot.add_cog(DecomposeDNSCommand(bot))
