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
    @commands.guild_only()
    @commands.has_any_role(*ROLES_PROF)
    @commands.check(isVoiceConnect)
    async def appel(self, ctx, *args):
        #On check si les rôles passés en arguments existent sur le serveur
        server_role = []
        for role in ctx.guild.roles:
            server_role.append(role.name)
        for arg in args:
            if arg not in server_role:
                await ctx.send("Un des rôles en paramètres n'existe pas sur ce serveur !",delete_after=ERROR_DELAY)
                await ctx.message.delete(delay=ERROR_DELAY)
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


def setup(client):
    client.add_cog(Teacher(client))
