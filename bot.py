from dotenv import load_dotenv
import os

import discord
from discord.ext import commands
import datetime

load_dotenv()

token = os.environ.get("TOKEN")

# --    ids    --
broadcasterUserID   = 676627205974917130        # could be changed to a list, currently just Franki

broadcastChannel    = 1176394849193304117       # channel for the broadcaster to put the command into

# --    bot instancing    --
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --    functions    --
def tprint(message):                            # just for timestamps
    print(str(datetime.datetime.utcnow()), str(message))

def parse_outputChannelID(message_content):
    # Extract the channel mention from the channel mention syntax
    # e.g., "!announce #general Hello!" -> "#general"
    return message_content.split(' ', 2)[1]

# --    setup    --
@bot.event
async def on_ready():
    print(f'{bot.user.name} ready for delivery!')

@bot.command()
async def post(ctx):
    required_role = discord.utils.get(ctx.guild.roles, name='broadcaster')
    # check if message is from the Franki/someone with the 'broadcaster' role and in the restricted channel
    if (ctx.author.id == broadcasterUserID or required_role in ctx.author.roles) and ctx.channel.id == broadcastChannel:

        # extract the output channel id from the broadcaster's message
        outputChannelID = parse_outputChannelID(ctx.message.content) 

        # get the output channel
        outputChannel = discord.utils.get(bot.get_all_channels(), mention=outputChannelID)

        # check if the message has content before sending
        if ctx.message.content.split(' ') != ctx.message.content.split(' ')[0:2]:

            # parse the message content after the command and channel mention
            announcement_message = ctx.message.content.split(' ', 2)[-1]
            tprint(f"@{ctx.author} -> {outputChannel}: {announcement_message}")

            # send the announcement to the output channel
            sent_message = await outputChannel.send(announcement_message)

        # send attached images
        for attachment in ctx.message.attachments:
            image_url = attachment.url
            await outputChannel.send(image_url)

bot.run(token)