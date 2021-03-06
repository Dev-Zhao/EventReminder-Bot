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
        params = {"userID": ctx.message.author.id}
        response = requests.get("https://event-reminder-discord-bot.herokuapp.com/authorize", params=params)

        data = response.json()
        newUser = {"userID": str(ctx.message.author.id), "authorization_url": str(data['authorization_url'])}
        self.googleevents.insert_one(newUser)

        await ctx.message.author.send("Please give authorization to access your Google Calendar")
        await ctx.message.author.send(data['authorization_url'])

    #commands
    @commands.command(aliases = ['calendar'])
    async def listCalendarEvents(self, ctx):
        params = {"userID": ctx.message.author.id}
        response = requests.get("https://event-reminder-discord-bot.herokuapp.com/calendar", params=params)

        if response.status_code == 404:
            await ctx.message.author.send("Use the 'import' command first")
        else:
            embed = discord.Embed(title="Your Google Calendar Events", color=0xf3c4ea)
            embed.set_author(name="Scheduler Bot | Created for RUHacks 2021",
                             icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")
            while True:
                events = response.json()
                count = 0
                for event in events['items']:
                    if "summary" in event and "description" in event and "start" in event and "dateTime" in event["start"]:
                        embed_field = (f"\n -------| {event['summary']} |------- \n Time: {event['start']['dateTime']} - {event['end']['dateTime']} \n {event['description']}")
                        embed.add_field(name=f"Event{count}", value=f"```{embed_field}```", inline=False)
                        count += 1
                        if count == 5:
                            break

                page_token = events.get('nextPageToken')
                if not page_token:
                    break

            await ctx.send(f"<@{ctx.message.author.id}>")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(GoogleAPI(client))