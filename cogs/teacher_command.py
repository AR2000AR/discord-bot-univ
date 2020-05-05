import discord
from discord.ext import commands


class Teacher(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Master", "Professeur")
    async def appel(self, ctx, args):
        list_group = []
        list_connected = []
        args = args.upper()

        if args != "TP1" and args != "TP2" and args != "TP3" and args != "TP4":
            await ctx.send("C'est pas un groupe !")
            return

        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send("Tu n'est pas dans un channel !")
            return

        await ctx.send(f"Appel dans le channel {channel.name}")
        print("Requête d'appel via !appel")

        # recuperer tous les membres d'un groupe
        for mem in ctx.guild.members:
            for role in mem.roles:
                if role.name == args:
                    list_group.append(mem)

        # recuperer tous les membres connecté au channel
        for eleve in channel.members:
            list_connected.append(eleve.name)

        i = 0
        appel_message = ""
        # afficher si ils sont preésent
        for pres in list_group:
            if pres.name in list_connected:
                appel_message += f"`{pres.nick} ({pres.name})` est présent :green_circle:\n"
            else:
                """user = self.client.get_user(pres.id)
                await user.send('Tu as cours sur discord "COMPUTING UNIVERSITY')"""
                appel_message += f"`{pres.nick} ({pres.name})` est absent :red_circle:\n"

                i += 1
        await ctx.send(appel_message + "\n" + f"Il y a {i} absent(s)")
        print(appel_message)

    @appel.error
    async def appel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("Erreur de requête via !appel : Manque le groupe en argument")
            await ctx.send("Tu dois précisez le groupe dont tu veux faire l'appel !")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Master ou Professeur pour utiliser cette commande !")

    @commands.command()
    @commands.has_any_role("Master", "Professeur")
    async def sujet(self, ctx):
        the_message = await ctx.send("A quel sujet en êtes vous ?")
        await the_message.add_reaction("zeroUL:706771494977404939")
        await the_message.add_reaction("unUL:706771880693989386")
        await the_message.add_reaction("deuxUL:706771912784871464")
        await the_message.add_reaction("troisUL:706771937103315004")
        await the_message.add_reaction("quatreUL:706771969281884170")
        await the_message.add_reaction("cinqUL:706771998419714088")
        await the_message.add_reaction("sixUL:706772029646569524")
        await the_message.add_reaction("septUL:706772056888442920")
        await the_message.add_reaction("huitUL:706772079109865522")
        await the_message.add_reaction("neufUL:706772105194373140")

    @sujet.error
    async def sujet_error(self, ctx, error):
        print("Erreur dans la requête via !sujet : Pas le bon rôle")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Master ou Professeur pour utiliser cette commande !")


def setup(client):
    client.add_cog(Teacher(client))
