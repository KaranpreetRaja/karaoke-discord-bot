import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

path_to_env = os.path.join(os.path.dirname(__file__), '.env')

# get the discord token from the .env file
load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
Channel = os.getenv('CHANNEL_ID')

intent = discord.Intents.default()
intent.message_content = True


ctx = commands.Context

client = commands.Bot(command_prefix='!', intents=intent)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # send message in spam channel
    channel = client.get_channel(Channel)
    await channel.send('Bot is online!')


# !play command to play music
@client.command()
async def play(ctx, *args):
    if not args:
        await ctx.send('Please enter a song and artist name in the format `!play {song} by {artist}`')
        return
    
    # join tuple args into a string and split by ' by '

    args = ' '.join(args).split(' by ')
    if len(args) != 2:
        await ctx.send('Please enter a song and artist name in the format `!play {song} by {artist}`')
        return

    # TODO: get auto and lyrics
    
    await ctx.send(f'Playing {args[0]} by {args[1]}!')

# !pause command to pause music
@client.command()
async def pause(ctx):

    # TODO: pause music

    await ctx.send('Pausing music!')

# !start command to start music that has been paused
@client.command()
async def start(ctx):
    #TODO: start music
    await ctx.send('Starting music again!')

client.run(Token)