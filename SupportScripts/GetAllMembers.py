import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import DiscordKey
import FunctionFile

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
    #AFKChannel = discord.utils.get(msg.server.channels, name='AFK', type=discord.ChannelType.voice)

    if CmdWord.startswith('ping') and msg.author.id != client.user.id:
        await client.send_message(msg.channel,":ping_pong: Pong!")
        invite = await  client.create_invite(msg.server, xkcd=True, max_uses = 1)
        await client.send_message(msg.author, invite)
        await asyncio.sleep(3)


@client.event
async def on_member_join():
    print("A member Joined")



client.run(DiscordKey.getDiscordKey())