import discord
from discord.ext import commands
from consts import *


def isVoiceConnect(ctx):
    try:
        channel = ctx.message.author.voice.channel
        return True
    except AttributeError:
        return False


class Teacher(commands.Cog):
    """Classe contenant toutes les commandes utiles pour les professeurs"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(*ROLES_PROF)
    @commands.check(isVoiceConnect)
    async def appel(self, ctx, *args):
        #On check si les rôles passés en arguments existent sur le serveur
        server_role = []
        for role in ctx.guild.roles:
            server_role.append(role.name)
        for arg in args:
            if arg not in server_role:
                await ctx.send("Un des rôles en paramètres n'existe pas sur ce serveur !")
                return #on ne veut pas continuer

        rolesMembers = []
        for member in ctx.guild.members:
            for memberRole in member.roles:
                if(memberRole.name in args):
                    if(member not in rolesMembers):
                        rolesMembers.append(member)
                        break #pas besoin de verifier les autres roles du membre

        message = ""
        nbAbs = 0

        for member in rolesMembers:
            if(member not in ctx.message.author.voice.channel.members):
                message += f'<@{member.id}> est absent :red_circle:\n'
                nbAbs+=1
        for member in rolesMembers:
            if(member in ctx.message.author.voice.channel.members):
                message += f'<@{member.id}> est présent :green_circle:\n'

        embed = discord.Embed(title="Appel",description=f'{message} \n Il y a {nbAbs} absent(s)')

        await ctx.send(embed=embed)

    @appel.error
    async def appel_error(self, ctx, error):
        if(isinstance(error,commands.MissingAnyRole)):
            await ctx.send("missing role",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)
        elif(isinstance(error,commands.CheckFailure)):
            await ctx.send("Pas dans un salon vocal",delete_after=ERROR_DELAY)
            await ctx.message.delete(delay=ERROR_DELAY)

    @commands.command()
    async def sondage_multiple(self, ctx, *args):
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

        emoji_number = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣", "9️⃣"]
        args = list(args)
        number_ans = int(args[0])

        del args[0]

        the_message = await ctx.send(" ".join(args))

        for i in range(0, number_ans):
            await the_message.add_reaction(emoji_number[i])

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

        await the_message.add_reaction("\U0001f7e2")
        await the_message.add_reaction("\U0001f534")


def setup(client):
    client.add_cog(Teacher(client))
