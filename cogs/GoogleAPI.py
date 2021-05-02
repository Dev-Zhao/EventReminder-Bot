import discord
import requests
from discord.ext import commands
import pymongo
import os


class GoogleAPI(commands.Cog):
    '''Manage your Google Calendar events!'''
    def __init__(self, client):
        self.client = client
        self.DBCRED = os.environ.get("DBCRED")
        self.database = pymongo.MongoClient(self.DBCRED)["ruhacks"]
        self.googleevents = self.database["googleevents"]

    #commands
    @commands.command(aliases = ['import'])
    async def importFromGoogle(self, ctx):
        params = {"_id": ctx.message.author.id}
        response = requests.get("https://event-reminder-discord-bot.herokuapp.com/authorize", params=params)

        data = response.json()
        newUser = {"_id": str(ctx.message.author.id), "authorization_url": str(data['authorization_url'])}
        self.googleevents.insert_one(newUser)

        await ctx.message.author.send("Please give authorization to access your Google Calendar")
        await ctx.message.author.send(data['authorization_url'])

    #commands
    @commands.command(aliases = ['calendar'])
    async def listCalendarEvents(self, ctx):
        await ctx.message.author.send("hi")


def setup(client):
    client.add_cog(GoogleAPI(client))