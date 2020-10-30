# module de base
import json

import discord
# import requests
from discord.ext import commands
from discord import Intents
# fonction musicale (os utile que pour ca atm)
from consts import TOKEN, GUILD
import os

#Merci à Maxime M pour l'info sur l'intent
intents = Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)
client.remove_command("help")

# gestion de l'erreur en cas de commande inconnue
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("Erreur dans la requête d'une commande : Commande inconnue")
        await ctx.send("Commande inexistante !")
    else:
        pass
        #raise error

# notification terminal de connexion
@client.event
async def on_ready():
    guild = "Inconnu"
    for guild in client.guilds:
        print(f'{client.user} has connected to' f' {guild.name} id: {guild.id}')

    await client.change_presence(activity=discord.Game(name="LvkwbjjBwmwgwpfvbURQ:cheh"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if(filename.startswith('fun')):
            continue
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
