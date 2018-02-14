import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
from discord import opus
import sys
import FunctionFile
import random
import DiscordKey


#######Get Constants ######
SimpleAudioDict = FunctionFile.getSimpleAudioDict()
SimpleAudioList = FunctionFile.getSimpleAudioList()
RngAudioDict = FunctionFile.getrngAudioDict()
RngAudioList = FunctionFile.getRngAudioList()

#for keys,values in SimpleAudioDict.items():
#    print(keys)
#    for keys2,value2 in SimpleAudioDict[keys].items():
#        print("\t" + keys2 + "\t:\t" + value2)



# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = discord.Client()


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

    if sys.maxsize > 2 ** 32:
        opus.load_opus('libopus-0.x64.dll')
    else:
        opus.load_opus('libopus-0.x86.dll')


# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.event
async def on_message(msg):
    CmdWord = FunctionFile.ConvertMsg(msg.content)
    if CmdWord.startswith('ping') and msg.author.id != client.user.id:
        await client.send_message(msg.channel,":ping_pong: Pong!")
        await asyncio.sleep(3)

    #removethis!!
    #if CmdWord.startswith('thisisatest') and FunctionFile.checkVoiceChannelFromMsg(msg, client):
    #    await client.send_message(msg.channel,"ernie sound!")
    #    try:
    #        voice = await client.join_voice_channel(msg.author.voice_channel)
    #        player = voice.create_ffmpeg_player('sounds/are you guys oh nevermind.wav')
    #        player.start()
    #    except:
    #        pass
    #    while True:
    #        try:
    #            if player.is_done():
    #                await voice.disconnect()
    #                break
    #        except:
    #            break

    if any(CmdWord in s for s in SimpleAudioList) and FunctionFile.checkVoiceChannelFromMsg(msg, client):
        print(SimpleAudioDict['logword'][CmdWord])
        try:
            await client.send_message(msg.channel, SimpleAudioDict['chatresponse'][CmdWord])
        except:
            pass
        try:
            voice = await client.join_voice_channel(msg.author.voice_channel)
            player = voice.create_ffmpeg_player(SimpleAudioDict['audiofile'][CmdWord])
            player.start()
        except:
            pass
        while True:
            try:
                if player.is_done():
                    await voice.disconnect()
                    break
            except:
                break

    if any(CmdWord in s for s in RngAudioList) and FunctionFile.checkVoiceChannelFromMsg(msg, client):
        RandomValue = random.randint(0,9)
        ChannelMessage = RngAudioDict['chatresponse'][CmdWord][RandomValue]
        AudioFile = RngAudioDict['audiofile'][CmdWord][RandomValue].lstrip()
        MoveChannel = RngAudioDict['kicktable'][CmdWord][RandomValue]
        print(RngAudioDict['logword'][CmdWord] + "\tRNGValue " + str(RandomValue) + "\tMove Channel = " + str(MoveChannel))

        try:
            await client.send_message(msg.channel, ChannelMessage)
        except:
            pass
        try:
            voice = await client.join_voice_channel(msg.author.voice_channel)
            player = voice.create_ffmpeg_player(AudioFile)
            player.start()
        except:
            pass
        while True:
            try:
                if player.is_done():
                    if MoveChannel == 'true':
                        await client.move_member(msg.author, msg.server.afk_channel)
                    await voice.disconnect()
                    break
            except:
                break

    if CmdWord.startswith('killme') and FunctionFile.checkVoiceChannelFromMsg(msg, client):
        print("Kill Me - " + msg.author.name)
        await client.send_message(msg.channel,"R I P")
        try:
            voice = await client.join_voice_channel(msg.author.voice_channel)
            player = voice.create_ffmpeg_player('sounds/killme.mp3')
            player.start()
        except:
            pass
        while True:
            try:
                if player.is_done():
                    await client.move_member(msg.author, msg.server.afk_channel)
                    await voice.disconnect()
                    break
            except:
               break

client.run(DiscordKey.getDiscordKey())

