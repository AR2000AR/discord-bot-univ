import discord
from discord.ext import commands
from consts import annee, roles

class Teacher(commands.Cog):
    
    """Classe contenant toutes les commandes utiles pour les professeurs"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def appel(self, ctx, *args):
        allowed_role = [] # array contenant tous les rôles du serveur pouvant éxécuter la commande
        # On fait la liste des rôles autorisés à utiliser cette commande
        for role in ctx.guild.roles:
            if role.name.startswith("Enseignant") or role.name.startswith("Admin"):
                allowed_role.append(role)

        # On vérifie que l'utilisateur a le droit d'utiliser la commande
        allowedUser = False

        for role in ctx.author.roles:
            if role in allowed_role:
                allowedUser = True
                break
        
        if not allowedUser:
            await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande !")
            return

        # Initialisation des variables
        server_role = [] # array contenant tous les rôles du serveur
        list_group = [] # array contenant tous les membres ayant les rôles dont on veut faire l'appel
        list_connected = [] # array contenant tous les mebres connectés au serveur vocal dont on vaut faire l'appel



        # On ajoute les roles présent sur le serveur dans une lsite
        for role in ctx.guild.roles:
            server_role.append(role.name)
        
        # On check si les rôles passés en arguments existent sur le serveur
        for arg in args:
            if arg not in server_role:
                await ctx.send("Un des rôles en paramètres n'existe pas sur ce serveur !")
        
        # On check si l'auteur du message est bien connecté à un salon vocal
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send("Tu n'es pas dans un salon vocal !")
            return
        
        # Message de requête
        await ctx.send(f"Appel dans le salon vocal {channel.name}")
        print("Requête d'appel via !appel")
        


        # On récupère tous les membres d'un groupe
        countRoles = len(args)
        for member in ctx.guild.members:
            countMem = 0
            for role in member.roles:
                if role.name in args:
                    countMem += 1
            if countMem == countRoles:
                list_group.append(member)


        # On récupère tous les membres connecté au channel
        for eleve in channel.members:
            list_connected.append(eleve.name)

        # décalaration des variables utilisés pour crééer les message
        i = 0
        appel_message = ""
        # ajoute la présence de la personne dans le message qui va être envoyé
        for present in list_group:
            if present.name in list_connected:
                appel_message += f"`{present.nick} ({present.name})` est présent :green_circle:\n"
            else:
                appel_message += f"`{present.nick} ({present.name})` est absent :red_circle:\n"

                i += 1

        # envoi du message
        await ctx.send(appel_message + "\n" + f"Il y a {i} absent(s).")

    @appel.error
    async def appel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("Erreur de requête via !appel : Manque le groupe en argument")
            await ctx.send("Tu dois précisez le groupe dont tu veux faire l'appel !")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Tu dois être Master ou Professeur pour utiliser cette commande !")

    @commands.command()
    async def sondage(self, ctx, *args):
        allowed_role = [] # array contenant tous les rôles du serveur pouvant éxécuter la commande
        # On fait la liste des rôles autorisés à utiliser cette commande
        for role in ctx.guild.roles:
            if role.name.startswith("Enseignant") or role.name.startswith("Admin"):
                allowed_role.append(role)

        # On vérifie que l'utilisateur a le droit d'utiliser la commande
        allowedUser = False

        for role in ctx.author.roles:
            if role in allowed_role:
                allowedUser = True
                break
        
        if not allowedUser:
            await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande !")
            return


        the_message = await ctx.send(" ".join(args))
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

    


def setup(client):
    client.add_cog(Teacher(client))
