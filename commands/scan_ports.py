import discord
from discord.ext import commands
import socket

class ScanPortsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="scan_ports", description="Scanne les ports ouverts d'une adresse IP.")
    async def scan_ports(self, ctx, ip: str, port_range: str = "1-1024"):
        await ctx.respond(f"Scan des ports pour `{ip}` en cours...")
        try:
            start, end = map(int, port_range.split('-'))
            open_ports = []
            for port in range(start, end + 1):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    if s.connect_ex((ip, port)) == 0:
                        open_ports.append(port)

            result = ", ".join(map(str, open_ports)) if open_ports else "Aucun port ouvert trouvé."
            await ctx.edit(content=f"Ports ouverts pour `{ip}` : {result}")
        except ValueError:
            await ctx.respond("Erreur : Plage de ports invalide.")

def setup(bot):
    bot.add_cog(ScanPortsCommand(bot))
