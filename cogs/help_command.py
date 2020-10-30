import discord
from discord.ext import commands
from consts import *

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def sendHelpMP(self, ctx, message):
        await ctx.send("Regarde tes MP",delete_after=MP_DELAY)
        await ctx.message.author.send(message)
        await ctx.message.delete(delay=MP_DELAY)

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):
        TITLE= "**Aide :**--------------------------------------------------------------------------------------------------------------------------------"
        LINE = "--------------------------------------------------------------------------------------------------------------------------------------"
        COMMON_HELP = \
            "**Commandes globales :**\n"\
            "    `!arche` - Donne le lien de arche\n"\
            "    `!ent` - Donne le lien vers l'ENT\n"\
            "    `!appel (rôle)` - Fait l'appel dans le channel de l'auteur de la commande affiche les présents, les absents, et le nombre d'absents \n"\
            "    `!sondage (question)` - Crée un sondage avec comme réponse possible oui ou non\n"\
            "    `!sondage_multiple (nombre de réponses) (question)` - Crée un sondage avec plusieurs réponses possibles numéroté (de 1 à 9 à vous de le définir)\n"
        TEACHER_HELP = \
            "**Commandes enseignant :**\n"\
            "    `!clear (nombre)` - Supprime les messages dans le channel actuelle\n"
        ADMIN_HELP = \
            "**Commmandes admin :**\n"\
            "    `!setgame (jeu)` - Change le jeu du bot\n"

        message = TITLE+"\n"+COMMON_HELP

        user = ctx.message.author
        isTeacher = False
        for role in user.roles:
            if(role.name in ROLES_PROF):
                isTeacher = True
                break

        if(isTeacher):
            message+=TEACHER_HELP

        if(user.guild_permissions.administrator):
            if(not isTeacher):
                message+=TEACHER_HELP
            message+=ADMIN_HELP

        message+=LINE

        await self.sendHelpMP(ctx,message)

    # commande ! arche
    @commands.command()
    @commands.guild_only()
    async def arche(self, ctx):
        await self.sendHelpMP(ctx,
        "----------------------------------------------------------\n"
        f"Voici le lien vers Arche : {LIEN_ARCHE}\n"
        "----------------------------------------------------------")

    # commande ! ent
    @commands.command()
    @commands.guild_only()
    async def ent(self, ctx):
        await self.sendHelpMP(ctx,
        "----------------------------------------------------------\n"
        f"Voici le lien vers l'ENT : {LIEN_ENT}\n"
        "----------------------------------------------------------")

def setup(client):
    client.add_cog(Help(client))
