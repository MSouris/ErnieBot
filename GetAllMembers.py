import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random
import os
import DiscordKey
import FunctionFile
import VoteClass

MemRoleDict = FunctionFile.getMembersRolesDict()
KickRoleList = FunctionFile.getKickRolesList()
VoteKickDict = {}

client = discord.Client()


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    for server in client.servers:
        if server.name == 'BotTest-Sissynerd':
            pass
        for member in server.members:
            name = member.name
            roleList = []
            for role in member.roles:
                if role.name != "@everyone" and member.name != 'ErniesChair':
                    roleList.append(role.name)
                    #print(name + "\t" + role.name)
            if len(roleList) > 0:
                #print(name + "\t" + ','.join(roleList))
                pass

@client.event
async def on_message(msg):
    CmdWord = FunctionFile.ConvertMsg(msg.content)
    if msg.author.id != client.user.id:
        print("Cmd = " + CmdWord)

    if CmdWord.startswith('ping') and msg.author.id != client.user.id:
        AFKChannel = discord.utils.get(msg.server.channels, name='AFK', type=discord.ChannelType.voice)
        await client.send_message(msg.channel,":ping_pong: Pong!")
        invite = await client.create_invite(AFKChannel, xkcd=True, max_age=82800, max_uses = 1)
        await client.send_message(msg.author, invite)

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
                    player = voice.create_ffmpeg_player('sounds/VoteKick/' + random.choice(os.listdir('sounds/VoteKick')))
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

    if CmdWord.startswith('!votekick') and msg.author.id != client.user.id:

        mentionList = msg.mentions

        AFKChannel = discord.utils.get(msg.server.channels, name='AFK', type=discord.ChannelType.voice)

        for mentionie, VotedUserStruct in VoteKickDict.copy().items():
            if VotedUserStruct.has5minpassed():
                print("Vote time expired for vote against " + VotedUserStruct.VotedUser.name)
                VoteKickDict.pop(mentionie, None)

        for mentionie, VotedUserStruct in VoteKickDict.copy().items():
        #    if VotedUserStruct.VotedUser.voice_channel is None:
        #        print("User " + VotedUserStruct.VotedUser.name + " is no longer in the channel")
        #        VoteKickDict.pop(VotedUserStruct, None)
            VotedUserStruct.removeUserWhoNoLongerAreInChannel(mentionie.voice_channel.voice_members)
            if VotedUserStruct.VotedUserSize == 0:
                print("Removing vote for " + VotedUserStruct.VotedUser.name + " because there are no more valid votes.")
                VoteKickDict.pop(mentionie, None)

        if len(mentionList) > 0:
            mentionie = mentionList[0]
            if mentionie in VoteKickDict:
                VoteKickDict[mentionie].addVotingUser(msg.author, len(msg.author.voice_channel.voice_members))
            else:
                if msg.author.voice_channel == mentionie.voice_channel:
                    VoteKickDict[mentionie] = VoteClass.VoteKick_struct(mentionie, msg.author, len(msg.author.voice_channel.voice_members))
                    await client.send_message(msg.channel, "Vote Kick started against - " + mentionie.name)
                else:
                    await client.send_message(msg.author, "You must be in a voice channel with the voted user.")

        else:
            await client.send_message(msg.author, "Not user mentioned in this vote kick")
            print(msg.author.name + " - vote kicked incorrectly '" + msg.content + "'.")

        for mentionie, VotedUserStruct in VoteKickDict.copy().items():
            if VotedUserStruct.hasNeededVoteSizeBeenMet(len(msg.author.voice_channel.voice_members)):
                print(VotedUserStruct.VotedUser.name + " has been vote kicked!!!")
                try:
                    voice = await client.join_voice_channel(msg.author.voice_channel)
                    player = voice.create_ffmpeg_player('sounds/VoteKick/' + random.choice(os.listdir('sounds/VoteKick')))
                    player.start()
                except:
                    pass
                while True:
                    try:
                        if player.is_done():
                            await voice.disconnect()
                            for mentionie in mentionList:
                                await client.send_message(msg.channel, "The tribe has spoken " + mentionie.mention)
                                await client.send_message(mentionie, "You have been vote kicked from the server. Click the invite below to get back into the server.")
                                invite = await client.create_invite(AFKChannel, xkcd=True, max_age=82800, max_uses=1)
                                await client.send_message(mentionie, invite)
                                await client.kick(mentionie)
                                VoteKickDict.pop(mentionie, None)
                            break
                    except:
                        break

    if CmdWord.startswith('!votestatus') and msg.author.id != client.user.id:
        if len(VoteKickDict) != 0:
            for mentionie, VotedUserStruct in VoteKickDict.copy().items():
                VotedUserStruct.removeUserWhoNoLongerAreInChannel(mentionie.voice_channel.voice_members)
                if VotedUserStruct.VotedUserSize == 0:
                    print("Removing vote for " + VotedUserStruct.VotedUser.name + " because there are no more valid votes.")
                    VoteKickDict.pop(mentionie, None)
                if VotedUserStruct.has5minpassed():
                    print("Vote time expired for vote against " + VotedUserStruct.VotedUser.name)
                    VoteKickDict.pop(mentionie, None)

            for mentionie, VotedUserStruct in VoteKickDict.items():
                print("Vote Kick - " + VotedUserStruct.VotedUser.name + " - " + str(VotedUserStruct.VotedUserSize) + "/" + str(VotedUserStruct.NeededVoted))
                print("\tvotes by:")
                for voter in VotedUserStruct.VotingUserList:
                    print("\t\t" + voter.name)
                await client.send_message(msg.channel, "Vote Kick - " + VotedUserStruct.VotedUser.name + " - " + str(VotedUserStruct.VotedUserSize) + "/" + str(VotedUserStruct.NeededVoted))
        if len(VoteKickDict) == 0:
            await client.send_message(msg.channel, "No active votes")




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