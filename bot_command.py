import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio
import pokepy
import cat



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
        "|`!pingmaster (demande)` - Permet d'envoyer une courte demande en DM aux Masters (ils ne sont ni mentionnable, et ne regarde pas les DMs d'inconnu)\n"
        "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        "|`!helpadmin` - Not for you the plèbe\n"
        "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        "|`!play (titre)` - Connecte le bot au salon où vous êtes et joue le titre demandé\n"
        "|`!pause` - Met en pause le titre\n"
        "|`!resume` - Reprend la lecture du titre\n"
        "|`!volume (nombre)` - Règle le volume\n"
        "|`!leave` - Arrête le musqie et déconnecte le Bot\n"
        "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        "|`!pokemon (nom)` - Donne la fiche pokédex d'un pokémon (nom anglais seulement)\n"
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


@pingmaster.error
async def pingmaster_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Précise ta demande tel que : `!pingmaster Ceci est une demande")


# situation actuelle
@client.command()
async def who(ctx):
    await ctx.send(
        "Je suis Roboris Davin, le bot de ce serveur. Je ne connais absolument ce professeur qui aurait un nom similaire.")


"""FONCTION MUSICALE"""


@client.command(aliases=['paly', 'aply', 'plya', 'join'])
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

    # je prend le titre je separe cahque arg par un espace
    title_format = " ".join(title)

    # query sur youtube qui met dans un dict toutes les infomations de la premiere video trouvé
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:'{title_format}'",
                                download=False)

    # je met seulement les informations qui m'intéressse cad le titre et l'url
    dic = {
        'url': info['entries'][0]['webpage_url'],
        'artist': info['entries'][0]['title']
    }

    # je dl la video et convertit en mp3
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([dic['url']])

    # je la renomme en song.mp3 affin de pas galerer si on remet une musique
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, 'song.mp3')

    # je joue la musique et affiche un petit message
    player = voice.play(FFmpegPCMAudio("song.mp3"))
    await ctx.send(f"En train de Jouer `{dic['artist']}`")


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Précise le titre que tu veux jouer")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Tu n'es pas dans un channel ou tu n'a pas précisé de titre")


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


@volume.error
async def volume_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Précise le volume aue tu veux définir")


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Déconnécté de {channel}")


"""FONCTION FUNNY"""


# pokemon
@client.command()
async def pokemon(ctx, name: str):
    types = []
    abilities = []
    poke = []
    pokespe = []

    try:
        poke = pokepy.V2Client().get_pokemon(name)
        pokespe = pokepy.V2Client().get_pokemon_species(name)
    except:
        await ctx.send("Pokémon Inconnu")
        return

    print(poke.name)
    print(poke.weight)
    print(poke.height)

    for i in range(len(poke.types)):
        types.append(poke.types[i].type.name)
    print(types)

    for i in range(len(poke.abilities)):
        abilities.append(poke.abilities[i].ability.name)
    print(abilities)
    print(poke.id)
    print(pokespe.flavor_text_entries[5].flavor_text)

    embed = discord.Embed(
        title=poke.name.capitalize() + "/" + pokespe.names[6].name,
        description=pokespe.flavor_text_entries[5].flavor_text,
        colour=discord.Colour.red(),
    )

    embed.set_image(url=f"https://pokeres.bastionbot.org/images/pokemon/{poke.id}.png")
    embed.set_author(name="Pokédex",
                     icon_url="https://cdn.icon-icons.com/icons2/851/PNG/512/Pokedex_icon-icons.com_67530.png")
    embed.set_thumbnail(url=poke.sprites.front_default, )
    embed.add_field(name="Types", value="\n".join(types), inline=False)
    embed.add_field(name="Weight/Height", value=str(poke.weight) + "/" + str(poke.height), inline=True)
    embed.add_field(name="Abilities", value="\n".join(abilities), inline=True)
    embed.set_footer(text='Prof. Chen Information')

    await ctx.send(embed=embed)


@pokemon.error
async def pokemon_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Précise le pokémon dont tu veux la fiche")


@client.command()
async def cat(ctx):
    cat.getCat(directory="/cat_image", filename="cat")
    ctx.send(file=discord.File('cat_image/cat.png'))

"""GESTION D'EVENEMENT"""


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
