import discord
from discord.ext import commands
import asyncio
import json
import random

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('bot online')

async def getdata():
    data = json.load(open('bank.json', 'r'))
    return data

async def openaccount(user):
    data = await getdata()
    if str(user) in data:
        return False
    else:
        data[str(user)] = {}
        data[str(user)]['wallet'] = 100
        data[str(user)]['bank'] = 0
    with open('bank.json', 'w') as bank:
        json.dump(data, bank, indent=4)

async def adjust(user, acc, amt):
    await openaccount(user)
    data = await getdata()
    data[str(user)][acc] += int(amt)
    with open('bank.json', 'w') as bank:
        json.dump(data, bank, indent=4)
		
@client.command()
async def beg(ctx):
    begamt = random.randint(2,30)
    person = (random.choice(list(open('begperson.txt')))).replace('\n', '')
    await adjust(ctx.author.id, 'wallet', begamt)
    await ctx.send(f"{person} just gave you {begamt} coins!")

@client.command()
async def rob(ctx, member:discord.Member):
    await openaccount(str(ctx.author.id))
    await openaccount(str(member.id))
    data = await getdata()
    chance = random.randint(0,10)
    robamt = random.randint(2,30)
    if chance < 7:
        if robamt > int(data[str(ctx.author.id)]['wallet']):
            robamt = int(data[str(ctx.author.id)]['wallet'])
        await ctx.send(f"You stole {robamt} coins from {str(member.display_name)}!")
        await adjust(str(ctx.author.id),'wallet' , robamt)
        await adjust(str(member.id), 'wallet', robamt * -1)
    else:
        if robamt > int(data[str(ctx.author.id)]['wallet']):
            robamt = int(data[str(ctx.author.id)]['wallet'])
        await ctx.send(f"You paid out {robamt} to {str(member.display_name)} for an unsuccessful robbery...")
        await adjust(ctx.author.id, 'wallet', robamt*-1)
        await adjust(str(member.id), 'wallet', robamt)

client.run("ODA3MTIxOTI5NDEyNTQyNDg1.YBzY3w.X5TPnx4wDmBxAMLq0yZWW26Iea4")