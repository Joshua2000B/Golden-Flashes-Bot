#https://nextcordpy.readthedocs.io/en/latest/api.html
#API for nextcord.py


import nextcord
import asyncio
from datetime import *

FLAG_WORDS = []
try:
    file = open("moderation/FLAG_WORDS.txt",'r')
    FLAG_WORDS = eval(file.read())
    file.close()
except SyntaxError:
    print("Flag words list is empty.")


file = open("IDs.txt",'r')
exec(file.read())
file.close()

file = open("secret.txt",'r')
SECRET = eval(file.read())
file.close()

file = open("secret_command.txt",'r')
SECRET_COMMAND = file.read()
file.close()



DEBUG_MODE = False


class MyClient(nextcord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):

        # Ignore messages from the bot itself
        if(message.author.id == 883173756426670150):
            return

        # Scan for flag words
        #   Author is a webhook - ignore
        #if(type(message.author) == nextcord.User):
        #    print("Message from user?",message.author,":",message.content)
        if(type(message.author) != nextcord.User):# and message.guild.get_role(666697415704838154) not in message.author.roles and message.guild.get_role(875936240472567818) not in message.author.roles):
            check = message.content.lower()
            for word in FLAG_WORDS:
                if(word in check):
                    await self.get_channel(WARNINGS_ID).send("<@&666697415704838154> "+str(message.author)+" sent a message containing '"+word+"' in <#"+str(message.channel.id)+"> -> " + message.jump_url)

        # Check if a Needs Roles member sent a nextcord Invite Link
        if("https://nextcord" in message.content.lower()):
            need_role = message.guild.get_role(NEED_ROLE_ID)
            if(need_role in message.author.roles):
                await message.channel.send(message.author.mention + " You cannot post invite links until you assign yourself other server roles!")
                await message.delete()

        # Check for command
        if(message.content.startswith("/")):
            await self.process_commands(message)



    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here
        if(command == "/squ_ping"):# and message.channel.name == "staff"):
            await message.channel.send("pong!")

        #Easter Egg
        elif(command == SECRET_COMMAND):
            await self.secret_command(message)


    async def secret_command(self,message):
        command = message.content.split()
        if(len(command) != 1):
            return
        #print(str(message.channel))
        if(message.channel.id != BOT_COMMANDS_ID and message.channel.id != STAFF_ID):
            return

        delay = 1
        try:
            await message.delete()
        except:
            pass
        fort = await message.channel.send(SECRET[0])
        await asyncio.sleep(delay)
        for part in SECRET[1:-1]:      
            await fort.edit(content = part)
            await asyncio.sleep(delay)
        await asyncio.sleep(delay)
        await fort.edit(content = SECRET[-1], delete_after = 4)


    #ON_MEMBER_UPDATE
    async def on_member_update(self,before,after):
        #print(before)
        need_role = before.guild.get_role(NEED_ROLE_ID)
        if(len(before.roles) == 2 and before.roles[1] == need_role and len(after.roles) > 2):
            await before.guild.get_member(before.id).remove_roles(need_role,reason="Removing Default Role",atomic=True)

        serious_role = before.guild.get_role(SERIOUS_ROLE_ID)
        if(serious_role in after.roles and serious_role not in before.roles):
            try:
                dm = await after.create_dm()
                await dm.send("""Now that you have access to venting, you are agreeing to the potential risks of the channel.
Triggering content like ||self harm, suicidal thoughts/attempts||, as well as other potentially dark topics.

When using venting, it might be helpful to use this tag system by starting your post with one of the following emojis to cue to others what you are venting for as it can help prevent miscommunication:
🗣️ means **Seeking Advice/Help**
🙏 means **Seeking Thoughts and Prayers**
💛 means **Seeking Love and Support**
👂 means **Seeking a Listening Ear**

In addition to using the above tags, please be mindful of when people do not. If someone does not use the tags above and you are unsure what they are seeking from this channel, then ask them. A simple “Are you looking for advice or just to vent?” or something similar is almost always sufficient. 

Sometimes people need help, sometimes people need advice, and sometimes people just need to be heard. Keeping these emojis in mind can help prevent offending someone or overstepping. 

Finally, if you choose to vent about potentially triggering content, please use two | symbols on both sides of the content that may trigger someone, and it will shade it out like my warning earlier. If others wish to read it, they can click it and the text will appear, but those who are potentially easily triggered will know not to click it and we can protect the members of our server.
❤️""")
            except nextcord.errors.Forbidden:
                print("Cannot DM",after.name)

    #WHEN READY
    async def on_ready(self):
        #await self.change_presence(activity=nextcord.Game(name = "game"))
        print("Successfully set Bot's game status")


    #CONNECTION
    async def on_connect(self):
        await super().on_connect()
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Starting Bot")
bot = MyClient(intents=nextcord.Intents.all())

@bot.slash_command()
async def send_anonmessage(interaction: nextcord.Interaction, msg: str):

    
    if(interaction.channel.id != ANONMESSAGE_ID and interaction.channel.id != BOT_COMMANDS_ID):
        #print(type(interaction.channel))
        if(type(interaction.channel) != nextcord.PartialMessageable):
            await interaction.response.send_message("Anonmessages can't be sent here!",ephemeral=True)
            return

    await interaction.response.send_message("Message Sent!",ephemeral=True)

    id_use = ANONMESSAGE_ID# if not DEBUG_MODE else 

    await interaction.client.get_channel(ANONMESSAGE_ID).send(msg)
    await interaction.client.get_channel(LOGS_ID).send(f"""The following anonmessage was sent by {interaction.user.mention}:
    
{msg}""")    




file = open("TOKEN.txt",'r')
TOKEN = file.read()
#print(TOKEN)
bot.run(TOKEN)
