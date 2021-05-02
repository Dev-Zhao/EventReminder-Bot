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
        # arg1 = time in military hours XX:YY
        # args = event details

        if bool(re.match("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", arg1)):
            users = self.database["users"]

            newUser = { "userID" : ctx.message.author.id , "event_time" : arg1 , "event_details": args }
            users.insert_one(newUser)
            embed=discord.Embed(title="New Event Created", color=0xf3c4ea)
            embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")
            embed.add_field(name = arg1, value= f"```{args}```")
            await ctx.send(embed = embed)

        else:
            await ctx.send(arg1 + " is an invalid arguement")


    ''' list a user's event'''
    @commands.command()
    async def listevent(self, ctx):

        user_events = list(self.database["users"].find({"userID" : ctx.message.author.id}, { "_id": 0 , "userID" : 0}))

        embed=discord.Embed(color=0xf3c4ea)
        embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")
        
        if not user_events:
            embed.add_field(name = "Empty Event List! ", value= "```Use *addevent <HH:MM> <Event Details> to schedule an event!```", inline=False)
        
        else:
            for event in user_events:
                embed.add_field(name = event.get('event_time') , value = f"```{event.get('event_details')}```", inline=False)

        await ctx.send(embed = embed)

    '''remove a user event'''
    @commands.command()
    async def removeevent(self, ctx, arg1):
        '''remove a users event taking place at a specific time, removes the first instance'''

        if bool(re.match("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", arg1)):
            users = self.database["users"]
            if (users.count_documents({"userID" : ctx.message.author.id , "event_time" : arg1}, limit = 1)) != 0:
                users.delete_one({"userID" : ctx.message.author.id , "event_time" : arg1})
                await ctx.send(f"{ctx.author.mention} deleted event at {arg1}!" )
            else:
                await ctx.send(f"{ctx.author.mention} You have no event at {arg1}!" )
        else:
            embed=discord.Embed(color=0xf3c4ea)
            embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")
            embed.add_field(name = "Invalid Format", value = "```Make sure your time is in the format HH:MM where 0 <= HH <= 24 and 0 <= MM <= 59 ```")
            await ctx.send(embed = embed)

            

def setup(bot):
    bot.add_cog(Scheduler(bot))


