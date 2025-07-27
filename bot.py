import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file

intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    #cek dan hapus tautan
    if "https://" in message.content:
        # simpan data pengguna
        print(f"user {message.author} ({message.author.id}) mengirim tautan: {message.content}")
        await message.delete()
        await message.channel.send("nggak boleh ngirim tautan di sini!")
        await message.guild.ban(message.author, reason="Mengirim tautan")

        await bot.process_commands(message)

        
@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

bot.run(token)