import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo

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
    async def addevent(self, ctx, arg1, arg2, arg3, arg4  ):
        users = self.database["users"]

        # arg1 = time in military hours XX:YY
        # arg2 = event name
        # arg3 = zoom link
        
        time = "12:34"

        if time.isdigit():

            #WORKJFHH BASFD 




        newUser = { "userID" : ctx.message.author.id , "event_name" : arg1 , "event_time": arg2 }

        x = users.insert_one(newUser)

        await ctx.send(x.inserted_id)

        # get event name

        event 


        




















def setup(bot):
    bot.add_cog(Scheduler(bot))


