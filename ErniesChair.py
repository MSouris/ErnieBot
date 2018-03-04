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
MemRoleDict = FunctionFile.getMembersRolesDict()
KickRoleList = FunctionFile.getKickRolesList()

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
    if msg.channel.type == discord.ChannelType.text:
        AFKChannel = discord.utils.get(msg.server.channels, name='AFK', type=discord.ChannelType.voice)

    if CmdWord.startswith('ping') and msg.author.id != client.user.id:
        await client.send_message(msg.channel,":ping_pong: Pong!")
        await asyncio.sleep(3)

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

    if any(CmdWord in s for s in RngAudioList) and FunctionFile.checkVoiceChannelFromMsg(msg, client) and (AFKChannel is not None):
        RandomValue = random.randint(0,9)
        ChannelMessage = RngAudioDict['chatresponse'][CmdWord][RandomValue]
        AudioFile = RngAudioDict['audiofile'][CmdWord][RandomValue].lstrip()
        MoveChannel = RngAudioDict['kicktable'][CmdWord][RandomValue]
        print(RngAudioDict['logword'][CmdWord] + "\tRNGValue " + str(RandomValue) + "\tMove Channel = " + str(MoveChannel))

        try:
            await client.send_message(msg.channel, str(RandomValue + 1) + " - " + ChannelMessage)
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
                        await client.move_member(msg.author, AFKChannel)
                    await voice.disconnect()
                    break
            except:
                break

    if CmdWord.startswith('killme') and FunctionFile.checkVoiceChannelFromMsg(msg, client) and (AFKChannel is not None):
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
                    await client.move_member(msg.author, AFKChannel)
                    await voice.disconnect()
                    break
            except:
               break

    if CmdWord.startswith('!rngesus') and FunctionFile.checkVoiceChannelFromMsg(msg, client) and (AFKChannel is not None):
        RandomNum = random.randint(0,9)
        print("RNGesus - " + str(RandomNum + 1) + " - " + msg.author.name)
        if RandomNum == 0:
            moveduser = random.choice(msg.author.voice_channel.voice_members)
            await client.send_message(msg.channel, "Headshot!!!! See ya " + moveduser.name)
            try:
                voice = await client.join_voice_channel(msg.author.voice_channel)
                player = voice.create_ffmpeg_player('sounds/CritHitRNG.mp3')
                player.start()
            except:
                pass
            while True:
                try:
                    if player.is_done():
                        await client.move_member(moveduser, AFKChannel)
                        await voice.disconnect()
                        break
                except:
                   break
        else:
            await client.send_message(msg.channel, "Bad aim. See ya " + msg.author.name)
            try:
                voice = await client.join_voice_channel(msg.author.voice_channel)
                player = voice.create_ffmpeg_player('sounds/Sniper_Fire_Reload.mp3')
                player.start()
            except:
                pass
            while True:
                try:
                    if player.is_done():
                        await client.move_member(msg.author, AFKChannel)
                        await voice.disconnect()
                        break
                except:
                   break

    if CmdWord.startswith('!kick') and msg.author.id != client.user.id:
        if FunctionFile.getRoleInListBool(msg.author.roles, KickRoleList) == False:
            await client.send_message(msg.author, "You do not have permissions to kick.")
            print(msg.author.name + " - does not have permission to kick '" + msg.content + "'.")
        else:
            AFKChannel = discord.utils.get(msg.server.channels, name='AFK', type=discord.ChannelType.voice)
            mentionList = msg.mentions
            if len(mentionList) > 0:
                try:
                    voice = await client.join_voice_channel(msg.author.voice_channel)
                    player = voice.create_ffmpeg_player('sounds/hasta-la-vista-baby.mp3')
                    player.start()
                except:
                    pass
                while True:
                    try:
                        if player.is_done():
                            await voice.disconnect()
                            for mentionie in mentionList:
                                await client.send_message(msg.channel, "Goodbye " + mentionie.mention)
                                await client.send_message(mentionie, "You have been kicked from the server. Click the invite below to get back into the server.")
                                invite = await client.create_invite(AFKChannel, xkcd=True, max_age=82800, max_uses=1)
                                await client.send_message(mentionie, invite)
                                await client.kick(mentionie)
                            break
                    except:
                        break
            else:
                await client.send_message(msg.author, "Not users mentioned in this kick")
                print(msg.author.name + " - kicked incorrectly '" + msg.content + "'.")


@client.event
async def on_member_join(member):
    print("A member joined - " + member.name)
    try:
        RoleNameList = MemRoleDict[member.name]
        for MemRoleName in RoleNameList:
            MemRoleObj = discord.utils.get(member.server.roles, name=MemRoleName)
            await client.add_roles(member, MemRoleObj)
            await client.send_message(member, "I've added you back to the role of " + MemRoleName + ".")
        print("Added - " + member.name + " - to roles - " + str(RoleNameList))
    except KeyError:
        print(member.name + "\t not in Member Role Dict or Role Config File!!!!!!!!!!!!!")


client.run(DiscordKey.getDiscordKey())
