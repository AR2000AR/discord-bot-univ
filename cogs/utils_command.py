import discord
from discord.ext import commands
from consts import *

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ADMIN COMMANDE"""
    # commande ! clear
    @commands.command()
    @commands.has_any_role(*ROLES_PROF, "Admin")
    async def clear(self, ctx, arg="0"):
        print("Requête de clear via !clear")
        await ctx.channel.purge(limit=int(arg)+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Enseignant pour utiliser cette commande !",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)

    # commande ! helpadmin
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def helpadmin(self, ctx):
        await ctx.send("Regarde tes MP", delete_after=MP_DELAY)
        await ctx.message.author.send("-----------------------------------------------------------------------------\n"
                       "`!clear (nombre)` - Supprime les messages dans le channel actuelle\n"
                       "`!setgame (jeu)` - Change le jeu du bot\n"
                       "-----------------------------------------------------------------------------")
        await ctx.message.delete(delay=MP_DELAY)

    # gestion de l'erreur en cas de non-possesion de master
    @helpadmin.error
    async def helpadmin_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            print("Erreur dans la requête via !helpadmin : Pas le bon rôle")
            await ctx.send("Tu dois être Admin pour utiliser cette commande !",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)

    @commands.command()
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

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Regarde tes MP", delete_after=MP_DELAY)
        await ctx.message.author.send(
            "----------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "|`!arche` - Donne le lien de arche\n"
            "|`!ent` - Donne le lien vers l'ENT\n"
            "|`!appel (rôle)` - Fait l'appel dans le channel de l'auteur de la commande affiche les présents, les absents, et le nombre d'absents \n"
            "|`!sondage (question)` - Crée un sondage avec comme réponse possible oui ou non\n"
            "|`!sondage_multiple (nombre de réponses) (question)` - Crée un sondage avec plusieurs réponses possibles numéroté (de 1 à 9 à vous de le définir)\n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------\n"
            )
        await ctx.message.delete(delay=MP_DELAY)

    # commande ! arche
    @commands.command()
    async def arche(self, ctx):
        await ctx.send("Regarde tes MP", delete_after=MP_DELAY)
        await ctx.message.author.send("----------------------------------------------------------\n"
                       f"Voici le lien vers Arche : {LIEN_ARCHE}\n"
                       "----------------------------------------------------------")
        await ctx.message.delete(delay=MP_DELAY)

    # commande ! ent
    @commands.command()
    async def ent(self, ctx):
        await ctx.send("Regarde tes MP", delete_after=MP_DELAY)
        await ctx.message.author.send("----------------------------------------------------------\n"
                       f"Voici le lien vers l'ENT : {LIEN_ENT}\n"
                       "----------------------------------------------------------")
        await ctx.message.delete(delay=MP_DELAY)

def setup(client):
    client.add_cog(Utils(client))
