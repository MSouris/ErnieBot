import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import DiscordKey
import FunctionFile

MemRoleDict = FunctionFile.getMembersRolesDict()
KickRoleList = FunctionFile.getKickRolesList()

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
                print(name + "\t" + ','.join(roleList))
                pass

@client.event
async def on_message(msg):
    CmdWord = FunctionFile.ConvertMsg(msg.content)

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
                    player = voice.create_ffmpeg_player('../sounds/hasta-la-vista-baby.mp3')
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