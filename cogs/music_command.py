import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['paly', 'aply', 'plya', 'join'])
    async def play(self, ctx, *title: str):
        print(f"Requête de chanson via !play, titre : {title} par {ctx.author}")
        # vérification du channel vocal : si le user est connecté -> récupération de l'instance de voix -> connexion ou move du bot

        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("Connecte toi dans un channel vocal")
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)
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
                os.rename(file, 'song.mp3')

        # je joue la musique et affiche un petit message
        player = voice.play(FFmpegPCMAudio("song.mp3"))
        await ctx.send(f"En train de Jouer `{dic['artist']}`")

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("Erreur dans la requête via !play : Manque le titre")
            await ctx.send("Précise le titre que tu veux jouer")
        if isinstance(error, commands.CommandInvokeError):
            print("Erreur dans la requête via !play : Utilisateur n'est pas dans un channel")
            await ctx.send("Tu n'es pas dans un channel ou tu n'a pas précisé de titre")

    @commands.command()
    async def pause(self, ctx):
        print("Requête de pause de la chanson via !pause")
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("Connecte toi dans un channel vocal")
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Musique mis en pause")
        else:
            await ctx.send("Aucune musique en cours")

    @commands.command()
    async def resume(self, ctx):
        print("Requête de reprise de la chanson via !resume")
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("Connecte toi dans un channel vocal")
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice:
            voice.resume()
            await ctx.send("Musique rejoue !")
        else:
            await ctx.send("Aucune musique en cours")

    @commands.command()
    async def volume(self, ctx, vol: float):
        """Changer le volume"""
        print("Requête de changement de volume de la chanson via !volume")
        if ctx.voice_client is None:
            return await ctx.send("Je ne suis pas connectée")

        ctx.voice_client.source.volume = vol / 100
        await ctx.send("Nouveau volume à {}%".format(vol))

    @volume.error
    async def volume_error(self, ctx, error):
        print("Erreur dans la requête de volume via !volume : Manque le volume en argument")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Précise le volume que tu veux définir")

    @commands.command(aliases=['stop'])
    async def leave(self, ctx):
        print("Requête de fin de la chanson via !leave")
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Déconnécté de {channel}")


def setup(client):
    client.add_cog(Music(client))
