import discord
from discord.ext import commands
import asyncio
import json
from constants import TOKEN
import random

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('bot online')


@client.command()
async def beg(ctx):
    begamt = random.randint(2,30)
    person = (random.choice(list(open('begperson.txt')))).replace('\n', '')
    await adjust(ctx.author, 'wallet', begamt)
    await ctx.send(f"{person} just gave you {begamt} coins!")


async def getdata():
    data = json.load(open('bank.json', 'r'))
    return data


async def openaccount(user):
    data = await getdata()
    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['wallet'] = 100
        data[str(user.id)]['bank'] = 0
    with open('bank.json', 'w') as bank:
        json.dump(data, bank)


async def adjust(user, acc, amt):
    await openaccount(user)
    data = await getdata()
    data[str(user.id)][acc] += int(amt)
    with open('bank.json', 'w') as bank:
        json.dump(data, bank)

client.run(TOKEN)