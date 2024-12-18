import discord
from discord.ext import commands

class UserInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="userinfo", description="Affiche des informations sur un utilisateur.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Informations sur {member.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Rejoint le", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="Rôles", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]))
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UserInfoCommand(bot))
