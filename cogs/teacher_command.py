import discord
from discord.ext import commands
import os


class Teacher(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Teacher(client))
