# module de base
import discord
from discord.ext import commands
from discord import Intents
from consts import *
import os
import webhook

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
        await ctx.send("Commande inexistante !",delete_after=ERROR_DELAY)
        await ctx.message.delete(delay=ERROR_DELAY)
    elif(isinstance(error, commands.NoPrivateMessage)):
        await ctx.send("Je ne répond pas aux messages privées")

# notification terminal de connexion
@client.event
async def on_ready():
    guild = "Inconnu"
    for guild in client.guilds:
        print(f'{client.user} has connected to' f' {guild.name} id: {guild.id}')

    await client.change_presence(activity=discord.Game(name=ACTIVITY))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f"Chargement de {filename}")
        client.load_extension(f'cogs.{filename[:-3]}')

edt = webhook.Edt(EDT_WEBHOOK,EDT_REFRESH,URL_ENT)
edt.start()

client.run(TOKEN)
