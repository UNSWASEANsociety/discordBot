import asyncio
import os
import discord
import random
import json
import uwuify
import dotenv
from boto.s3.connection import S3Connection

from src.emojify import emojify
from src.sheets import read_sheet

client = discord.Client()


def save_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, sort_keys=True, indent=4)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    response = None
    if message.author == client.user:
        return

    if not message.content.startswith('$'):
        return

    command = message.content.split(' ')

    if command[0] == '$help':
        response = '''
        **Command list:**
        ***help** - Show list of commands
        ***quote [thing]** - Get a random quote from list
        '''

    elif command[0] == '$quote':
        quotes = open('wordbank/ansafone.txt').read().splitlines()
        response = random.choice(quotes)

    elif command[0] == '$emojify':
        message = await message.channel.fetch_message(message.reference.message_id)
        response = emojify(message.content)

    elif command[0] == '$uwu':
        message = await message.channel.fetch_message(message.reference.message_id)
        response = uwuify.uwu(message.content, flags=uwuify.SMILEY)

    else:
        response = 'Command not found'

    await message.channel.send(response)


async def send_quotes():
    # assuming the bot is connected to only one guild
     guild = client.guilds[0]
     channel = random.choice(guild.text_channels)


async def love_letters(channel_id):
    await client.wait_until_ready()

    channel = client.get_channel(id=int(channel_id))
    with open('data/state.json', 'r') as f:
        state = json.load(f)

    n = state['RANT_NUM']
    while not client.is_closed():
        rants = read_sheet()
        if len(rants) > n:
            msg = f'**Rant #{n}** by {rants[n][1]}\n*{rants[n][2]}*\n'
            await channel.send(msg)

            n += 1
            state['RANT_NUM'] = n

            with open('data/state.json', 'w') as f:
                json.dump(state, f)

        await asyncio.sleep(600)


if __name__ == '__main__':
    if os.path.exists('.env'):
        dotenv.load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        channel_id = os.getenv('MAIN_CHANNEL')
    else:
        token = os.environ.get('DISCORD_TOKEN')
        channel_id = os.environ.get('MAIN_CHANNEL')
        
    
    client.loop.create_task(love_letters(channel_id))
    client.run(token)