
#from asyncio.windows_events import NULL
#from asyncio.windows_events import NULL

import os
import os.path
import discord
from discord.ext import commands
from discord import Embed
import time
import sqlite3
from typing import Optional
conn = sqlite3.connect('atlas.db')
print ("Opened database successfully");
print ("Ver 3.0");
print (os.getcwd())

intents = discord.Intents.default()

bot = commands.Bot(command_prefix = "?", intents = intents)


@bot.command()
#async def invites(ctx, member: discord.Member=None):
async def invites(ctx, member: Optional[discord.User]):  
 # v_ref_count_mem_ID = member.id
 # if v_ref_count_mem_ID is None:
  if member is None:
    v_ref_count_mem_ID = ctx.author.id
    v_surname = ctx.author.display_name
    v_avatar_url = ctx.author.avatar_url
  else :
    v_ref_count_mem_ID = member.id
    v_surname = member.display_name
    v_avatar_url = member.avatar_url
  cursor = conn.execute('select Ref_Count , Discord_ID from referral_log where Discord_ID=? limit 1',[v_ref_count_mem_ID])
  v_ref_mem_ID_invite = ''
  for row in cursor:
        v_ref_Tot_count = row[0] 
        v_ref_mem_ID_invite = row[1]
  if v_ref_mem_ID_invite == '':
    embed=discord.Embed(title="The User Does not have Referral Code, Use ?generate to generate code!", description= 'Use - ?generate', color=discord.Color.dark_grey())
    embed.set_author(name=v_surname, icon_url=v_avatar_url)
    await ctx.send(ctx.author.mention,embed=embed)
  else:
   embed=discord.Embed(title="Current Invites Redeemed:", description= v_ref_Tot_count, color=discord.Color.dark_grey())
   embed.set_author(name=v_surname, icon_url=v_avatar_url)
   await ctx.send(ctx.author.mention,embed=embed)
#    await ctx.send(v_ref_Tot_count)

@bot.command()
async def generate(ctx):
    v_discord_ID = ctx.author.id
    v_ref_dup = ''
    cursor = conn.execute('select Ref_Count , Discord_ID from referral_log where Discord_ID=? limit 1',[v_discord_ID])
    for row in cursor:
          v_ref_dup = row[0] 
    if v_ref_dup != '':
      embed=discord.Embed(title="User can not generate more than one code!", description= 'Use - ?mycode to get your previously generated code', color=discord.Color.dark_grey())
      await ctx.send(ctx.author.mention,embed=embed)
    else:
      cursor = conn.execute("select Referral_ID, Discord_ID, Ref_Count from Referral_Log where Discord_ID IS NULL LIMIT 1")
      for row in cursor:

          v_referral_key = row[0] 
      
    # await print ("Operation done successfully")
      embed=discord.Embed(title="Referral code :", description= row[0], color=discord.Color.dark_grey())
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      await ctx.send(ctx.author.mention,embed=embed)
    

    # v_referral_key = row[2]
      cursor = conn.execute('''update Referral_Log set Discord_ID=? , Ref_Count = 0 where Referral_ID=?''',(v_discord_ID,v_referral_key))
      conn.commit()


@bot.command()
async def redeem(ctx, *, content:str):
  v_content = content
  v_dark_greylist = ctx.author.id
  v_Discord_dark_greylist = ''
  if time.time() - ctx.author.created_at.timestamp() < 1209600:
    embed=discord.Embed(title="The User is younger than 2 weeks.", description= 'You cannot redeem a code', color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(ctx.author.mention,embed=embed)
  else:
   # User can not redeem their own Code
    v_own_user_redeem = ''
    cursor = conn.execute('select Referral_ID from referral_log where Discord_ID=? limit 1',[v_dark_greylist])
    for row in cursor:
        v_own_user_redeem = row[0] 
    if v_own_user_redeem == v_content: 
        embed=discord.Embed(title="User cannot use their own Code!", description= v_own_user_redeem, color=discord.Color.dark_grey())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(ctx.author.mention,embed=embed)        
    else:       
      cursor = conn.execute('select Discord_ID from referral_used_id where Discord_ID=? limit 1',[v_dark_greylist])
      for row in cursor:
          v_Discord_dark_greylist = row[0] 
      if v_Discord_dark_greylist != '':
        
        #ctx.author.id in dark_greylist:
          embed=discord.Embed(title="User has already used a code!", description= "You've already used a code and cannot use another.", color=discord.Color.dark_grey())
          embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
          await ctx.send(ctx.author.mention,embed=embed)
      else:
          v_referral_key = ''

          cursor = conn.execute('select Referral_ID from Referral_Log where Referral_ID=?',[v_content])
          for row in cursor:
              v_referral_key = row[0] 
          if v_referral_key != '':
        # v_referral_key = content
        # v_referral_key = row[2]
            cursor = conn.execute('''update Referral_Log set Ref_Count = Ref_Count + 1 where Referral_ID=?''',[v_referral_key])
            conn.commit()   
        #Insert in Used List Table (dark_grey List) 
            cursor = conn.execute('''INSERT INTO Referral_Used_ID (Discord_ID) VALUES (?)''',[v_dark_greylist])
            conn.commit()        
            embed=discord.Embed(title="Code Accepted!", description= 'The code has been accepted', color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(ctx.author.mention,embed=embed)
          else:
            embed=discord.Embed(title="Code Rejected!", description= "The code is invalid/doesn't work.", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(ctx.author.mention,embed=embed)

@bot.command()
async def checkage(ctx):
  if time.time() - ctx.author.created_at.timestamp() < 1209600:
    await ctx.send("Younger than 2 weeks")
  else:
    await ctx.send("Good to go! Older than 2 weeks")

   
@bot.command()
async def userid(ctx, member: discord.User): 
  await ctx.send(member.id)

@bot.command()
async def commandlist(ctx):
  embed=discord.Embed(title="Command List", description="All Commands must be in lowercase \n \n ?mycode - shows your code. \n ?generate - generates code that you can share with friends. \n ?redeem (code) - This command followed by a code gives the codes owner an invite point. \n ?invites - shows how many invites you have \n", color=discord.Color.dark_grey())
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(ctx.author.mention,embed=embed) 

@bot.command()
async def mycode(ctx, member: Optional[discord.User]):  
    if member is None:
        v_ref_mycode_mem_ID = ctx.author.id
        v_mycode_surname = ctx.author.display_name
        v_mycode_avatar_url = ctx.author.avatar_url
    else :
        v_ref_mycode_mem_ID = member.id
        v_mycode_surname = member.display_name
        v_mycode_avatar_url = member.avatar_url
   # v_req_user_id = ctx.author.id
    v_own_user_Code = ''
    cursor = conn.execute('select Referral_ID from referral_log where Discord_ID=? limit 1',[v_ref_mycode_mem_ID])
    for row in cursor:
        v_own_user_Code = row[0] 
    if v_own_user_Code == '':
      embed=discord.Embed(description="This user doesn't have a code.\n \n -Use "'"?generate"'"  \n", color=discord.Color.dark_grey())
      embed.set_author(name=v_mycode_surname, icon_url=v_mycode_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed) 
    else:
      embed=discord.Embed(title="Generated code for :" + v_mycode_surname, description= v_own_user_Code, color=discord.Color.dark_grey())
      embed.set_author(name=v_mycode_surname, icon_url=v_mycode_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed)


@bot.command()
async def test(ctx):
  await ctx.send("test")


@bot.command()
@commands.has_permissions(administrator=True)
async def clearcode(ctx,  *, content:str):
   if content != '':
    v_ref_id = content
    cursor = conn.execute('''update Referral_Log  set discord_id = NULL , Ref_Count = NULL where Referral_ID=?''',[v_ref_id])
    conn.commit()   
    await ctx.send("Reset Data Complete for Referral ID " + content)
   else:
    await ctx.send("Referral ID is missing in command " + content)

@bot.command()
@commands.has_permissions(administrator=True)
async def totalredemptions(ctx):
    cursor = conn.execute('select sum(ref_count) from referral_log')
    for row in cursor:
        v_redemptions = row[0] 
    
    embed=discord.Embed(description="Total Redemptions : " +str(v_redemptions) , color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(ctx.author.mention,embed=embed) 

@bot.command()
@commands.has_permissions(administrator=True)
async def totalcodes(ctx):
    cursor = conn.execute('select count (discord_id) from referral_log')
    for row in cursor:
        v_totalcodes = row[0] 
    
    embed=discord.Embed(description="Total Codes Generated : " +str(v_totalcodes) , color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(ctx.author.mention,embed=embed) 

# Leader Board Command
@bot.command()
async def leaderboard(ctx):  
    
    cursor = conn.execute('select discord_id, Ref_count from  referral_log order by ref_count desc  limit 10')
    v_description_info = ""
    v_rank = 0
    for row in cursor:
        v_rank = v_rank + 1
        v_description_info += "**" +str(v_rank) + ". " + f"<@"+str(row[0])+">" + "**\n" + str(row[1]) + " Redemptions\n\n" 
    embed = discord.Embed(title="Leaderboard", description="Top 10", color=0x00ff00)
    embed=discord.Embed(description= v_description_info, color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(ctx.author.mention,embed=embed) 


#bot.run(os.getenv('TOKEN'))
