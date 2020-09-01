import discord
from discord.ext import commands



class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ADMIN COMMANDE"""
    # commande ! clear
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, arg):
        print("Requête de clear via !clear")
        await ctx.channel.purge(limit=int(arg)+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("Erreur de requête via !arche : Manque le nombre en argument")
            await ctx.send("Tu dois précisez le nombre de message que tu veux clear ! Exemple : !clear 10")
        if isinstance(error, commands.CheckFailure):
            print("Erreur de requête via !arche : Manque le nombre en argument")
            await ctx.send("Tu dois être Admin pour utiliser cette commande !")

    # commande ! helpadmin
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def helpadmin(self, ctx):
        print("Requête de helpadmin via !helpadmin")
        await ctx.send("-----------------------------------------------------------------------------\n"
                       "`!clear (nombre)` - Supprime les messages dans le channel actuelle\n"
                       "`!setgame (jeu)` - Change le jeu du bot\n"
                       "-----------------------------------------------------------------------------")

    # gestion de l'erreur en cas de non-possesion de master
    @helpadmin.error
    async def helpadmin_error(self, ctx, error):
        print("Erreur dans la requête via !helpadmin : Pas le bon rôle")
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Tu dois être Admin pour utiliser cette commande !")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgame(self, ctx, *args: str):
        print("Requête de changement de Game Status de bot via !setgame")
        await self.client.change_presence(activity=discord.Game(name=" ".join(args)))
        await ctx.send(f"Je joue désormais à " + " `" + " ".join(args) + "`")

    @setgame.error
    async def setgame_error(self, ctx, error):
        print("Erreur dans la requête via !setgame : Pas le bon rôle")
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Tu dois être Admin pour utiliser cette commande !")

    """FIN ADMIN COMMANDE"""

    # situation actuelle
    @commands.command()
    async def who(self, ctx):
        print("Requête de description du bot via !who")
        await ctx.send(
            "Je suis Roboris Davin, le bot de ce serveur. Je ne connais absolument pas ce professeur qui aurait un nom similaire.")

    @commands.command()
    async def help(self, ctx):
        print("Requête d'aide via !help")
        await ctx.send(
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "|`!arche` - Donne le lien de arche\n"
            "|`!ent` - Donne le lien vers l'ENT\n"
            "|`!who` - Fait découvir qui est Roboris Davin\n"
            "|`!appel (rôle)` - Fait l'appel dans le channel de l'auteur de la commande affiche les présents, les absents, et le nombre d'absents \n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            )

    # commande ! arche
    @commands.command()
    async def arche(self, ctx):
        print("Requête de lien arche via !arche")
        await ctx.send("----------------------------------------------------------\n"
                       "Voici le lien vers Arche : https://cutt.ly/tygWbO6\n"
                       "----------------------------------------------------------")

    # commande ! ent
    @commands.command()
    async def ent(self, ctx):
        print("Requête de lien de l'ent via !ent")
        await ctx.send("----------------------------------------------------------\n"
                       "Voici le lien vers l'ENT : https://cutt.ly/MygW3Rc\n"
                       "----------------------------------------------------------")



def setup(client):
    client.add_cog(Utils(client))
