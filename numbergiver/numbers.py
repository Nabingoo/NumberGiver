import os
import os.path
import discord
from discord.ext import commands
from discord import Embed
import time
import sqlite3
from typing import Optional
conn = sqlite3.connect('numbers.db')
print ("Opened database successfully");
print ("Ver 1.0");
print (os.getcwd())

intents = discord.Intents.default()

bot = commands.Bot(command_prefix = "+", intents = intents)


@bot.command()
@commands.has_permissions(administrator=True)
async def assign(ctx, member: Optional[discord.User], number):
    
    if member is None:
        v_discord_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar.url
        
    else:
        v_discord_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar.url
    v_ref_dup = ''
    
    
    
    cursor = conn.execute('select number , DiscordID from numberlist where DiscordID=? limit 1',[v_discord_ID])
    for row in cursor:
          v_ref_dup = row[0] 
    if v_ref_dup != '':
      
      cursor = conn.execute('''update numberlist set Number= ? where DiscordID=?''',[number,v_discord_ID])
      conn.commit()
      embed=discord.Embed(title="Assigned Number:", description= number, color=discord.Color.red())
      embed.set_author(name=v_surname)
      embed.set_thumbnail(url=v_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed)
    else:
      
      
      cursor = conn.execute('''INSERT INTO numberlist (DiscordID,number) VALUES (?,?)''',(v_discord_ID, number))
      conn.commit()

      embed=discord.Embed(title="Assigned Number:", description= number, color=discord.Color.red())
      embed.set_author(name=v_surname)
      embed.set_thumbnail(url=v_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed)

    
@bot.command()
async def number(ctx, member: Optional[discord.User]):  
    if member is None:
        v_ref_mycode_mem_ID = ctx.author.id
        v_mycode_surname = ctx.author.display_name
        v_mycode_avatar_url = ctx.author.avatar.url
    else :
        v_ref_mycode_mem_ID = member.id
        v_mycode_surname = member.display_name
        v_mycode_avatar_url = member.avatar.url
   # v_req_user_id = ctx.author.id
    v_own_user_Code = ''
    cursor = conn.execute('select number from numberlist where DiscordID=? limit 1',[v_ref_mycode_mem_ID])
    for row in cursor:
        v_own_user_Code = row[0] 
    if v_own_user_Code == '':
      embed=discord.Embed(description="This user doesn't have a number.\n \n talk to a staff member.  \n", color=discord.Color.red())
      embed.set_author(name=v_mycode_surname, icon_url=v_mycode_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed) 
    else:
      embed=discord.Embed(title="Player Number for : " + v_mycode_surname, description= v_own_user_Code, color=discord.Color.red())
      embed.set_author(name=v_mycode_surname, icon_url=v_mycode_avatar_url)
      await ctx.send(ctx.author.mention,embed=embed)
    

bot.run("OTYzNjE4MDQ0MzkzOTU1MzM4.YlYtPA.-DAHQMCQh8R4_oS4WvRitT4So0A")

  

    