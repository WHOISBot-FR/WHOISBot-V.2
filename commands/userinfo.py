import discord
from discord.ext import commands
from datetime import datetime

class UserInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="userinfo", description="Affiche des informations détaillées sur un utilisateur.")
    async def userinfo(self, ctx, user: discord.User):
        embed = discord.Embed(title="Informations sur l'utilisateur", color=discord.Color.blue())
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="Nom d'utilisateur", value=user.name, inline=True)
        embed.add_field(name="Discriminant", value=f"#{user.discriminator}", inline=True)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Bot", value="Oui" if user.bot else "Non", inline=True)

        embed.add_field(name="Compte créé le", value=user.created_at.strftime("%d/%m/%Y à %H:%M:%S"), inline=False)

        if isinstance(user, discord.Member):
            embed.add_field(name="Rejoint le serveur le", value=user.joined_at.strftime("%d/%m/%Y à %H:%M:%S") if user.joined_at else "Inconnu", inline=False)
            embed.add_field(name="Rôles", value=", ".join([role.mention for role in user.roles[1:]]) if len(user.roles) > 1 else "Aucun rôle", inline=False)

        embed.set_footer(text=f"Commande exécutée par {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.timestamp = datetime.utcnow()

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UserInfoCommand(bot))