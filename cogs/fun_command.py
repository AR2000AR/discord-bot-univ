import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import requests
import json


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


def setup(client):
    client.add_cog(Fun(client))
