import discord
from discord.ext import commands
from consts import masters


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ADMIN COMMANDE"""
    # commande ! clear
    @commands.command()
    @commands.has_any_role("Master")
    async def clear(self, ctx, arg):
        print("Requête de clear via !clear")
        await ctx.channel.purge(limit=int(arg))

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("Erreur de requête via !arche : Manque le nombre en argument")
            await ctx.send("Tu dois précisez le nombre de message que tu veux clear ! Exemple : !clear 10")
        if isinstance(error, commands.MissingAnyRole):
            print("Erreur de requête via !arche : Manque le nombre en argument")
            await ctx.send("Tu dois être Master pour utiliser cette commande !")

    # commande ! helpadmin
    @commands.command()
    @commands.has_any_role("Master")
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
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Master pour utiliser cette commande !")

    @commands.command()
    @commands.has_any_role("Master")
    async def setgame(self, ctx, *args: str):
        print("Requête de changement de Game Status de bot via !setgame")
        await self.client.change_presence(activity=discord.Game(name=" ".join(args)))
        await ctx.send(f"Je joue désormais à " + " `" + " ".join(args) + "`")

    @setgame.error
    async def setgame_error(self, ctx, error):
        print("Erreur dans la requête via !setgame : Pas le bon rôle")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Master pour utiliser cette commande ! 57 % de chance que ce soit Nicolas Bem qui ait essayé")

    """FIN ADMIN COMMANDE"""

    # ping les master
    @commands.command()
    async def pingmaster(self, ctx, *args):
        print("Requête d'une demande aux masters via !pingmaster")
        dm = " ".join(args)
        print(dm)

        if dm == "":
            await ctx.send("Précisez votre demande tel que : `!pingmaster Ceci est une demande`")
        else:
            for master in masters:
                user = self.client.get_user(master)
                await user.send(
                    'Demande de {} depuis le channel #{} et pour la demande suivante : "{}"'.format(ctx.author,
                                                                                                    ctx.channel.name,
                                                                                                    dm))
            await ctx.send("La demande est envoyée aux 3 Masters du Discord")

    @pingmaster.error
    async def pingmaster_error(self, ctx, error):
        print("Erreur dans la requête !pingmaster : Manque la demande en argument")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Précise ta demande tel que : `!pingmaster Ceci est une demande")

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
            "|`!github` - Donne le lien et les règles du GitHub\n"
            "|`!who` - Fait découvir qui est Roboris Davin\n"
            "|`!pingmaster (demande)` - Permet d'envoyer une courte demande en DM aux Masters (ils ne sont ni mentionnable, et ne regarde pas les DMs d'inconnu)\n"
            "|`!appel (groupe)` - Fait l'appel dans le channel de l'auteur de la commande affiche les présents, les absents, et le nombre d'absents \n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "|`!helpadmin` - Not for you the plèbe\n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "|`!play (titre)` - Connecte le bot au salon où vous êtes et joue le titre demandé\n"
            "|`!pause` - Met en pause le titre\n"
            "|`!resume` - Reprend la lecture du titre\n"
            "|`!volume (nombre)` - Règle le volume\n"
            "|`!leave` - Arrête le musique et déconnecte le Bot\n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "|`!pokemon (nom)` - Donne la fiche pokédex d'un pokémon (nom anglais seulement)\n"
            "|`!cat` - Image aléatoire de chat\n"
            "|`!dog` - Image aléatoire de chien\n"
            "|`!league (champion)` - Information de champion de League of Legends\n"
            "|`!meme` - Meme aléatoire\n"
            "|`!panda` - Image aléatoire de panda\n"
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")



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

    # commande !github
    @commands.command()
    async def github(self, ctx):
        print("Requête du lien github via !github")
        await ctx.send(
            "-----------------------------------------------------------------------------------------------------------------------------------------\n"
            "                                    Voici le lien vers le GitHub d'aide des INFO : https://cutt.ly/lyjQ8yr\n"
            "recopie interdite utilisez-le seulement pour comprendre ce que vous n'avez pas compris ou si vous avez loupé des cours\n"
            "-----------------------------------------------------------------------------------------------------------------------------------------")


def setup(client):
    client.add_cog(Utils(client))
