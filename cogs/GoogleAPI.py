import discord
import requests
from discord.ext import commands


class GoogleAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

    #commands
    @commands.command(aliases = ['import'])
    async def importFromGoogle(self, ctx):
        await ctx.send("hi")


def setup(client):
    client.add_cog(GoogleAPI(client))