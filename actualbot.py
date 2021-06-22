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
    await openaccount(ctx.author)
    begamt = random.randint(2, 30)
    person = (random.choice(list(open('begperson.txt')))).replace('\n', '')
    await adjust(ctx.author, 'wallet', begamt)
    await ctx.send(f"{person} just gave you {begamt} coins!")


@client.command()
async def test(ctx):
    data = await getdata()
    await ctx.send(data[str(ctx.author.id)]['wallet'])


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
        data[str(user.id)]['stock'] = {'aapl': [0, 0],'goog': [0, 0],'nflx': [0, 0],'fb': [0, 0],'amzn': [0, 0],'tsla': [0, 0],'baba': [0, 0],'nvda': [0, 0],'msft': [0, 0],'twtr': [0, 0],'gme': [0, 0],'btc-usd': [0, 0],'bch-usd': [0, 0],'ltc-usd)': [0, 0],'eth-usd': [0, 0],'bnb-usd': [0, 0],'link-usd': [0, 0],'doge-usd': [0, 0]}
    with open('bank.json', 'w') as bank:
        json.dump(data, bank, indent=4)

async def adjust(user, acc, amt):
    await openaccount(user)
    data = await getdata()
    data[str(user.id)][acc] += int(amt)
    with open('bank.json', 'w') as bank:
        json.dump(data, bank, indent=4)

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
        
client.run(TOKEN)
