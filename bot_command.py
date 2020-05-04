# module de base
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
# fonction musicale (os utile que pour ca atm)
import youtube_dl
import os
# pokemon

# cat and dog func






client = commands.Bot(command_prefix='!')
client.remove_command("help")


"""FONCTION DE COMMANDE VERS LE TEXTE"""




@client.command()
async def help(ctx):
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
        "|`!meme` - Meme aléatoire"
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


# commande ! helpadmin
@client.command()
@commands.has_any_role("Master")
async def helpadmin(ctx):
    print("Requête de helpadmin via !helpadmin")
    await ctx.send("-----------------------------------------------------------------------------\n"
                   "`!clear (nombre)` - Supprime les messages dans le channel actuelle\n"
                   "-----------------------------------------------------------------------------")


# gestion du rôle en cas de non-possesion de master
@helpadmin.error
async def helpadmin_error(ctx, error):
    print("Erreur dans la requête via !helpadmin : Pas le bon rôle")
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("Tu dois être Master pour utiliser cette commande !")


# commande ! arche
@client.command()
async def arche(ctx):
    print("Requête de lien arche via !arche")
    await ctx.send("----------------------------------------------------------\n"
                   "Voici le lien vers Arche : https://cutt.ly/tygWbO6\n"
                   "----------------------------------------------------------")


# commande ! ent
@client.command()
async def ent(ctx):
    print("Requête de lien de l'ent via !ent")
    await ctx.send("----------------------------------------------------------\n"
                   "Voici le lien vers l'ENT : https://cutt.ly/MygW3Rc\n"
                   "----------------------------------------------------------")


# commande !github
@client.command()
async def github(ctx):
    print("Requête du lien github via !github")
    await ctx.send(
        "-----------------------------------------------------------------------------------------------------------------------------------------\n"
        "                                    Voici le lien vers le GitHub d'aide des INFO : https://cutt.ly/lyjQ8yr\n"
        "recopie interdite utilisez-le seulement pour comprendre ce que vous n'avez pas compris ou si vous avez loupé des cours\n"
        "-----------------------------------------------------------------------------------------------------------------------------------------")


@client.command()
@commands.has_any_role("Master", "Professeur")
async def appel(ctx, args):
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

    ctx.send(f"Appel dans le channel {channel.name}")
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
    # afficher si ils sont preésent
    for pres in list_group:
        if pres.name in list_connected:
            await ctx.send(f"`{pres.nick} ({pres.name})` est présent :green_circle:")
        else:
            user = client.get_user(pres.id)
            await user.send('Tu as cours sur discord "COMPUTING UNIVERSITY')
            await ctx.send(f"`{pres.nick} ({pres.name})` est absent :red_circle:")

            i += 1

    await ctx.send(f"Il y a {i} absent(s)")


@appel.error
async def appel_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print("Erreur de requête via !appel : Manque le groupe en argument")
        await ctx.send("Tu dois précisez le groupe dont tu veux faire l'appel !")
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("Tu dois être Master ou Professeur pour utiliser cette commande !")




"""FONCTION MUSICALE"""


"""FONCTION FUNNY"""





@client.command()
@commands.has_any_role("Master", "Professeur")
async def sujet(ctx):
    the_message = await ctx.send("A quel sujet en êtes vous ?")
    emoji = discord.utils.get(ctx.guild.emojis, name='LUL')
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
async def sujet_error(ctx, error):
    print("Erreur dans la requête via !sujet : Pas le bon rôle")
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("Tu dois être Master ou Professeur pour utiliser cette commande !")


"""GESTION D'EVENEMENT"""


# gestion de l'erreur en cas de commande inconnue
@client.event
async def on_command_error(ctx, error):
    print("Erreur dans la requête d'une commande : Commande inconnue")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inexistante ! M. Davin aurait honte de toi !")
    else:
        raise error


# notification terminal de connexion
@client.event
async def on_ready():
    guild = "Inconnu"
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to' f' {guild.name} id: {guild.id}')
    user = client.get_user(214435319745871872)
    await user.send('Connecté prêt à fonctionner')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)
