import discord
from discord.ext import commands

class ConvertCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="convert", description="Convertit un nombre entre différentes bases.")
    async def convert(self, ctx, nombre: str, base_actuelle: int, base_voulue: int):
        try:
            decimal = int(nombre, base_actuelle)
            conversion = {
                2: bin(decimal)[2:],
                8: oct(decimal)[2:],
                10: str(decimal),
                16: hex(decimal)[2:].upper()
            }
            result = conversion.get(base_voulue, "Base non prise en charge.")
            await ctx.respond(f"Conversion de `{nombre}` (base {base_actuelle}) en base {base_voulue} : `{result}`")
        except ValueError:
            await ctx.respond("Erreur : Le nombre ou la base spécifiée est invalide.")

def setup(bot):
    bot.add_cog(ConvertCommand(bot))
