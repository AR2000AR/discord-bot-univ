# module de base
import json

import discord
import requests
from discord.ext import commands
# fonction musicale (os utile que pour ca atm)
from consts import TOKEN, GUILD
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


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
