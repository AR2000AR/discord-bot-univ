# module de base
import json

import discord
import requests
from discord.ext import commands
# fonction musicale (os utile que pour ca atm)
from consts import TOKEN, GUILD, FreezingKas, STICKOS
import os

client = commands.Bot(command_prefix='!')
client.remove_command("help")


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


@client.command()
async def sendv(ctx):
    await ctx.send("MESSAGE TEST")


@client.event
async def on_member_update(before, after):
    if after.id == STICKOS:
        for ac in after.activities:
            if ac.name == "Spotify":
                print("Changement de musique Yannis")
                message = await client.get_channel(707326525409591336).fetch_message(707326749297344655)
                print(ac.track_id)
                embed = discord.Embed(
                    title=ac.title,
                    description="Par **" + " ".join(ac.artists) + "**",
                    colour=ac.color,
                    url=f"https://open.spotify.com/track/{ac.track_id}",
                )

                embed.set_image(url=ac.album_cover_url)
                embed.set_thumbnail(url="https://zupimages.net/up/20/19/gbon.png")
                embed.add_field(name="Album", value=ac.album, inline=False)

                await message.edit(content="Vois ce qu'écoute S T I C K O S sur le channel radio-yannis", embed=embed)

    if after.id == FreezingKas:
        for ac in after.activities:
            if ac.name == "Spotify":
                print("Changement de musique Maxence")
                message = await client.get_channel(707326587074248726).fetch_message(707329464790679703)
                print(ac.track_id)
                embed = discord.Embed(
                    title=ac.title,
                    description="Par **" + " ".join(ac.artists) + "**",
                    colour=ac.color,
                    url=f"https://open.spotify.com/track/{ac.track_id}",
                )

                embed.set_image(url=ac.album_cover_url)
                embed.set_thumbnail(url="https://zupimages.net/up/20/19/gbon.png")
                embed.add_field(name="Album", value=ac.album, inline=False)
                await message.edit(content="Ce qu'écoute Maxence ", embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
