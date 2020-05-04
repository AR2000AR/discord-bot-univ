import discord
from discord.ext import commands
import requests
import json
import pokepy


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def panda(self, ctx):
        print("Requête d'image de panda via !panda")
        r = requests.get('https://some-random-api.ml/img/panda')

        json_data = json.loads(r.text)
        await ctx.send(json_data['link'])

    @commands.command()
    async def cat(self, ctx):
        print("Requête d'image de chat via !cat")
        r = requests.get('https://api.thecatapi.com/v1/images/search')

        json_data = json.loads(r.text)
        await ctx.send(json_data[0]['url'])

    @commands.command()
    async def dog(self, ctx):
        print("Requête d'image de chien via !dog")
        r = requests.get('https://dog.ceo/api/breeds/image/random')

        json_data = json.loads(r.text)
        await ctx.send(json_data['message'])

    @commands.command()
    async def meme(self, ctx):
        print("Requête d'image de meme via !meme")
        r = requests.get('https://meme-api.herokuapp.com/gimme')

        json_data = json.loads(r.text)
        await ctx.send(json_data['url'])

    # pokemon
    @commands.command()
    async def pokemon(self, ctx, name: str):
        print("Requête de pokémon via !pokemon")
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

        for i in range(len(poke.types)):
            types.append(poke.types[i].type.name)

        for i in range(len(poke.abilities)):
            abilities.append(poke.abilities[i].ability.name)

        embed = discord.Embed(
            title=poke.name.capitalize() + "/" + pokespe.names[6].name,
            description=pokespe.flavor_text_entries[6 if name == "pikachu" or name == "Pikachu" else 5].flavor_text,
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
    async def pokemon_error(self, ctx, error):
        print("Erreur dans la requête via !pokemon : Manque le pokemon en argument")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Précise le pokémon dont tu veux la fiche")

    @commands.command(aliases=['ligue'])
    async def league(self, ctx, name: str):
        print("Requête de champions de League of Legends via !league")
        name = name.capitalize()
        name = name.replace("'", "")
        # ntm riot
        if name == "Wukong":
            name = "MonkeyKing"


        r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/10.9.1/data/fr_FR/champion/{name}.json')
        json_data = json.loads(r.text)
        embed_lol = discord.Embed(
            title=json_data['data'][name]['name'] + ", " + json_data['data'][name]['title'],
            description=json_data['data'][name]['lore'],
            colour=discord.Colour.dark_blue(),
        )

        embed_lol.set_image(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_0.jpg")
        embed_lol.set_author(name="League of IUT",
                             icon_url="https://www.dlf.pt/png/big/25/252235_league-of-legends-logo-png.jpg")
        embed_lol.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/10.9.1/img/champion/{name}.png", )
        embed_lol.add_field(name="Passif", value=json_data['data'][name]['passive']['name'], inline=False)
        embed_lol.add_field(name="Q Spell", value=json_data['data'][name]['spells'][0]['name'], inline=True)
        embed_lol.add_field(name="W Spell", value=json_data['data'][name]['spells'][1]['name'], inline=True)
        embed_lol.add_field(name="E Spell", value=json_data['data'][name]['spells'][2]['name'], inline=True)
        embed_lol.add_field(name="Ultime", value=json_data['data'][name]['spells'][3]['name'], inline=True)

        await ctx.send(embed=embed_lol)

    @league.error
    async def league_error(self, ctx, error):
        print("Erreur dans la requête via !league : Manque le champion en argument")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Précise le champion dont tu veux la fiche !")


def setup(client):
    client.add_cog(Fun(client))
