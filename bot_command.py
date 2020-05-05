# module de base
import discord
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


@client.command()
async def sendv(ctx):
    await ctx.send("MESSAGE TEST")

@client.event
async def on_member_update(before, after):
    if after.id == 214435319745871872:
        for ac in after.activities:
            if ac.name == "Spotify":
                print(ac.title)
                print(ac.artists)
                message = await client.get_channel(705403811560423476).fetch_message(707312964310401054)

                embed = discord.Embed(
                    title=ac.title,
                    description="Par " + " ".join(ac.artists),
                    colour=ac.color,
                )

                embed.set_image(url=ac.album_cover_url)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/fr/6/60/Spotify_logo_sans_texte.png")
                await message.edit(content="La musique du moment de S T I C K O S", embed=embed)

    else:
        return



for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
