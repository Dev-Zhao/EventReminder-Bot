import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo
import re

class Scheduler(commands.Cog):
    '''Scheduler :0'''
    
    def __init__(self, bot):
        self.bot = bot

        load_dotenv()
        self.DBCRED = os.environ.get("DBCRED")

        self.database = pymongo.MongoClient(self.DBCRED)["ruhacks"]


    @commands.command()
    async def readylol(self,ctx):
        await ctx.send("hi it worked")
        await ctx.send(self.database.list_database_names())


    '''add a user'''
    @commands.command()
    async def addevent(self, ctx, arg1, *,args = None):
        users = self.database["users"]

        # arg1 = time in military hours XX:YY
        # args = event details

        if bool(re.match("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", arg1)):
            await ctx.send(arg1 + " is a valid arguement")
            newUser = { "userID" : ctx.message.author.id , "event_time" : arg1 , "event_details": args }
            users.insert_one(newUser)
            embed=discord.Embed(title="New Event Created", color=0xf3c4ea)
            embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")
            embed.add_field(name = arg1, value= args)
            await ctx.send(embed = embed)

        else:
            await ctx.send(arg1 + " is an invalid arguement")


    ''' list a user's event'''
    @commands.command()
    async def listevent(self, ctx):

        user_events = list(self.database["users"].find({"userID" : ctx.message.author.id}, { "_id": 0 , "userID" : 0}))

        embed=discord.Embed(title="Your Events", color=0xf3c4ea)
        embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")

        for event in user_events:
            embed.add_field(name = event.get('event_time') , value = event.get('event_details'), inline=False)

        await ctx.send(embed = embed)
            

def setup(bot):
    bot.add_cog(Scheduler(bot))


