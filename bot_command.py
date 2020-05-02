import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio



TOKEN = 'Njg4NDk0NzkzNDg3NDE3MzQ0.Xqw3jQ.m4xReJ6Oxek_gDnkKtvzi0isAdI'
GUILD = "COMPUTING UNVIVERSITY"

client = commands.Bot(command_prefix='!')
client.remove_command("help")

masters = (214435319745871872, 258246094788493312, 227497954389393408)

"""FONCTION DE COMMANDE VERS LE TEXTE"""


@client.command()
async def ping(ctx):
    await ctx.send('pong')


@client.command()
async def help(ctx):
    await ctx.send(
        "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        "|`!arche` - Donne le lien de arche\n"
        "|`!ent` - Donne le lien vers l'ENT\n"
        "|`!github` - Donne le lien et les règles du GitHub\n"
        "|`!who` - Fait découvir qui est Roboris Davin\n"
        "|`!pingmaster` - Permet d'envoyer une courte demande en DM aux Masters (ils ne sont ni mentionnable, et ne regarde pas les DMs d'inconnu)\n"
        "|`!helpadmin` - Not for you the plèbe\n"
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------")


# commande ! helpadmin
@client.command()
@commands.has_any_role("Master")
async def helpadmin(ctx):
    await ctx.send("-----------------------------------------------------------------------------\n"
                   "`!clear (nombre)` - Supprime les messages dans le channel actuelle\n"
                   "-----------------------------------------------------------------------------")


# gestion du rôle en cas de non-possesion de master
@helpadmin.error
async def helpadmin_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("Tu dois être Master pour utiliser cette commande !")


# commande ! arche
@client.command()
async def arche(ctx):
    await ctx.send("----------------------------------------------------------\n"
                   "Voici le lien vers Arche : https://cutt.ly/tygWbO6\n"
                   "----------------------------------------------------------")


# commande ! ent
@client.command()
async def ent(ctx):
    await ctx.send("----------------------------------------------------------\n"
                   "Voici le lien vers l'ENT : https://cutt.ly/MygW3Rc\n"
                   "----------------------------------------------------------")


# commande !github
@client.command()
async def github(ctx):
    await ctx.send(
        "-----------------------------------------------------------------------------------------------------------------------------------------\n"
        "                                    Voici le lien vers le GitHub d'aide des INFO : https://cutt.ly/tygWbO6\n"
        "recopie interdite utilisez-le seulement pour comprendre ce que vous n'avez pas compris ou si vous avez loupé des cours\n"
        "-----------------------------------------------------------------------------------------------------------------------------------------")


# commande ! clear
@client.command()
@commands.has_any_role("Master")
async def clear(ctx, arg):
    await ctx.channel.purge(limit=int(arg))


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Tu dois précisez le nombre de message que tu veux clear ! Exemple : !clear 10")
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("Tu dois être Master pour utiliser cette commande !")


# ping les master
@client.command()
async def pingmaster(ctx, *args):
    dm = " ".join(args)
    print(dm)

    if dm == "":
        await ctx.send("Précisez votre demande tel que : `!pingmaster Ceci est une demande`")
    else:
        for master in masters:
            user = client.get_user(master)
            await user.send('Demande de {} depuis le channel #{} et pour la demande suivante : "{}"'.format(ctx.author,
                                                                                                            ctx.channel.name,
                                                                                                            dm))
            await ctx.send("La demande est envoyée aux 3 Masters du Discord")


# situation actuelle
@client.command()
async def who(ctx):
    await ctx.send(
        "Je suis Roboris Davin, le bot de ce serveur. Je ne connais absolument ce professeur qui aurait un nom similaire.")


"""FONCTION MUSICALE"""


@client.command()
async def play(ctx, *title: str):
    # vérification du channel vocal : si le user est connecté -> récupération de l'instance de voix -> connexion ou move du bot
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Connecte toi dans un channel vocal")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    # check si un fichier n'existe pas déjà dans le répertoire
    song_there = os.path.isfile("song.mp3")

    if song_there:
        os.remove("song.mp3")

    # option de base pour le dl de la musqiue (modifiable si je trouve des trucs worth)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    el_title = " ".join(title)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:'{el_title}'",
                                download=False)

    dic = {
        'url': info['entries'][0]['webpage_url'],
        'artist': info['entries'][0]['title']
    }

    print(dic['url'])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([dic['url']])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, 'song.mp3')

    player = voice.play(FFmpegPCMAudio("song.mp3"))
    await ctx.send(f"En train de Jouer {dic['artist']}")


@client.command()
async def pause(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Connecte toi dans un channel vocal")
        return
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("Musique mis en pause")
    else:
        await ctx.send("Aucune musique en cours")


@client.command()
async def resume(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Connecte toi dans un channel vocal")
        return
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice:
        voice.resume()
        await ctx.send("Musique rejoue !")
    else:
        await ctx.send("Aucune musique en cours")


@client.command()
async def volume(ctx, vol: float):
    """Changer le volume"""

    if ctx.voice_client is None:
        return await ctx.send("Je ne suis pas connectée")

    ctx.voice_client.source.volume = vol / 100
    await ctx.send("Nouveau volume à {}%".format(vol))


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Déconnécté de {channel}")


# gestion de l'erreur en cas de commande inconnue
@client.event
async def on_command_error(ctx, error):
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


client.run(TOKEN)
