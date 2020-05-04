import discord
from discord.ext import commands
import os
import consts.masters

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

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


def setup(client):
    client.add_cog(Utils(client))
