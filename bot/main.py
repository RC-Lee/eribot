import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import func

load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")
MONGOURL = os.getenv("MONGO_URL")

cluster = MongoClient(MONGOURL)
db = cluster["DiscordData"]
collection = db["UserData"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild.me.permissions_in(message.channel).read_messages:
        return
    if not message.guild.me.permissions_in(message.channel).send_messages:
        return
    
    if message.content.startswith('$re'):
        myquery = {"_id": message.author.id}
        if(collection.count_documents(myquery) == 0):
            post = {"_id": message.author.id, "name": message.author.name, "eventRoll": [{"r": 0, "star":0, "name": "", "imgUrl": "", "type":""}], "eiRoll": [{"r": 0, "star":0, "name": "", "imgUrl": "", "type":""}], "normalRoll": [{"r": 0, "star":0, "name": "", "imgUrl": "", "type":""}], "event4Pity": 0, "ei4Pity": 0, "normal4Pity": 0, "event5Pity": 0, "ei5Pity": 0, "normal5Pity": 0 }
            collection.insert_one(post)
        
        user = collection.find(myquery)
        if message.content == '$re':
            tData = await func.rollEvent(user[0])
            collection.update_one({"_id": tData["_id"]}, {"$set": {"eventRoll": tData["eventRoll"], "event4Pity": tData["event4Pity"], "event5Pity":tData["event5Pity"]}})

            rTitle = "You rolled a " + str(tData["eventRoll"][-1]["star"]) + " star item"
            embed = discord.Embed(title=rTitle, color=discord.Color.purple())
            embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
            if not tData["eventRoll"][-1]["imgUrl"] == "":
                embed.set_image(url=tData["eventRoll"][-1]["imgUrl"])
            embed.set_footer(text="Roll #" + str(tData["eventRoll"][-1]["r"]))
            await message.channel.send(embed=embed)

        if message.content == '$re10':
            embed = discord.Embed(title="Making 10 wishes", color=discord.Color.orange())
            embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
            temp = {}
            for i in range(0,10):
                tData = await func.rollEvent(user[0])
                collection.update_one({"_id": tData["_id"]}, {"$set": {"eventRoll": tData["eventRoll"], "event4Pity": tData["event4Pity"], "event5Pity":tData["event5Pity"]}})
                embed.add_field(name="Roll " + str(tData["eventRoll"][-1]["r"]) +": ", value= tData["eventRoll"][-1]["name"], inline=False)
                if(tData["eventRoll"][-1]["star"] >= 4):
                    if(temp):
                        if(tData["eventRoll"][-1]["star"] > temp["star"]):
                            temp = tData["eventRoll"][-1]
                    else:
                        temp = tData["eventRoll"][-1]
            if(temp):
                embed.set_image(url=temp["imgUrl"])
                embed.set_footer(text=temp["name"] + " from Roll#" + str(temp["r"]))
            await message.channel.send(embed=embed)

    if message.content.startswith('$le'):
        myquery = {"_id": message.author.id}
        if(collection.count_documents(myquery) == 0):
            await message.channel.send("You haven't rolled yet")
            return
    
        user = collection.find(myquery)
        tempList = []
        embed = discord.Embed(title="Listing", color=discord.Color.red())
        if message.content == '$le':
            tempList = user[0]["eventRoll"][-25]
            embed = discord.Embed(title="Listing (last 25) 4 and 5 star event", color=discord.Color.red())
        elif message.content == '$le4':
            tempList = func.get4(user[0]["eventRoll"])[-25]
            embed = discord.Embed(title="Listing (last 25) 4-star event", color=discord.Color.red())
        elif message.content == '$le5':
            tempList = func.get5(user[0]["eventRoll"])[-25]
            embed = discord.Embed(title="Listing (last 25) 5-star event", color=discord.Color.red())
        elif message.content == '$lec':
            tempList = func.getC(user[0]["eventRoll"])[-25]
            embed = discord.Embed(title="Listing (last 25) 4 and 5 star character rolls from event", color=discord.Color.red())
        elif message.content == '$lew':
            tempList = func.getC(user[0]["eventRoll"])[-25]
            embed = discord.Embed(title="Listing (last 25) 4 star weapon rolls from event", color=discord.Color.red())
        else: 
            return

        embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
        for roll in tempList:
            if(roll["star"] >= 4 ):
                embed.add_field(name="Roll " + str(roll["r"]) +": ", value=roll["name"], inline=False)
        embed.set_footer(text="If you don't see anything, you haven't rolled a 4 or 5 star yet")
        await message.channel.send(embed=embed)
    
    if message.content == '$help':
        embed = discord.Embed(title="List of commands", color=discord.Color.green())
        embed.add_field(name="$re", value="Roll once on the event banner", inline=False)
        embed.add_field(name="$re10", value="Roll ten times on the event banner", inline=False)
        embed.add_field(name="$le", value="List 4 and 5 star rolls from event banner. (Last 25)", inline = False)
        embed.add_field(name="$le4", value="List 4-star rolls from event banner. (Last 25)", inline = False)
        embed.add_field(name="$le5", value="List 5-star rolls from event banner. (Last 25)", inline = False)
        embed.add_field(name="$lec", value="List 4 and 5 star character rolls from event banner. (Last 25)", inline = False)
        embed.add_field(name="$lew", value="List 4 star weapon rolls from event banner. (Last 25)", inline = False)
        await message.channel.send(embed = embed)
    
    
client.run(TOKEN)