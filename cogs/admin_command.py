import discord
from discord.ext import commands
from consts import *

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ADMIN COMMANDE"""
    # commande ! clear
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(*ROLES_PROF, *ROLE_ADMIN)
    async def clear(self, ctx, arg="0"):
        print("Requête de clear via !clear")
        await ctx.channel.purge(limit=int(arg)+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Enseignant pour utiliser cette commande !",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setgame(self, ctx, *args: str):
        print("Requête de changement de Game Status de bot via !setgame")
        await self.client.change_presence(activity=discord.Game(name=" ".join(args)))
        await ctx.send(f"Je joue désormais à " + " `" + " ".join(args) + "`")

    @setgame.error
    async def setgame_error(self, ctx, error):
        if isinstance(error, commands.MissingPermission):
            print("Erreur dans la requête via !setgame : Pas le bon rôle")
            await ctx.send("Tu dois être Admin pour utiliser cette commande !",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)

    """FIN ADMIN COMMANDE"""

def setup(client):
    client.add_cog(Utils(client))
