import discord
import requests
from discord.ext import commands


class GoogleAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

    #commands
    @commands.command(aliases = ['import'])
    async def importFromGoogle(self, ctx):
        response = requests.get("https://event-reminder-discord-bot.herokuapp.com/authorize")
        data = response.json()
        await ctx.send(data['authorization_url'])


def setup(client):
    client.add_cog(GoogleAPI(client))