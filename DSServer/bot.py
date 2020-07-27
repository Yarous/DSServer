import discord
from discord.ext import commands
from discord.utils import get
import os
from time import sleep
import requests

prefix = '!'
client = commands.Bot( command_prefix = prefix )
client.remove_command( 'help' )

bad_words = [ 'уёбок', 'тварь', 'сука', 'ебать' ]

#Words 
#.help
#https://discord.gg/hPXvtQ

@client.event 

async def on_ready():
	print( 'BOT Conected!' )

	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Minecraft' ) )


@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
@client.event
async def on_message( message ):
	await client.process_commands( message )

	msg = message.content.lower()

	if msg in bad_words:
		await message.delete()
		await message.author.send( f'{ message.author } Пожалуйста не пишите такие слова,за это вам могут дать бан!')

@client.event 
async def on_command_error( ctx, error ):
	pass

@client.event 

async def on_member_join( member ):
	channel = client.get_channel( 731467673422266370 )

	role = discord.utils.get( member.guild.roles, id = 731545957883445253 )

	await member.add_roles( role )
	await channel.send( f'Привет { member.mention }!') 

@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Mute' )

	await member.add_roles( mute_role )
	await ctx.send( f'У { member.mention }, очграничение доступа к чату, за нарушение прав!' )

@mute.error 
async def mute_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды mute!')
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)
async def help( ctx ):
	emb = discord.Embed( title = 'Навигация по командам')

	emb.add_field( name = '{}clear'.format( prefix ), value = 'Очистка чата!' )
	emb.add_field( name = '{}kick'.format( prefix ), value = 'Кик участника!' )
	emb.add_field( name = '{}ban'.format( prefix ), value = 'Бан пользователя!' )
	emb.add_field( name = '{}unban'.format( prefix ), value = 'Удаление орграничений у конкретного пользователя к серверу!' )

	await ctx.send( embed = emb )
@help.error 
async def help_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды help!')

@client.command( pass_context = True )
@commands.has_permissions( administrator = True)
async def unban( ctx, *, member):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user
		await ctx.guild.unban( user )
		await ctx.send( f'Unbanned user {user.mention} ')

		return
@unban.error 
async def unban_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды unban!')

	


@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def clear ( ctx, amount : int ):
	await ctx.channel.purge( limit = amount )


@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды clear!')



@commands.has_permissions( administrator = True )
@client.command( pass_context = True )
async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )
	await member.send( f'Вас кикнул { ctx.author.mention } по неизвестной мне причине все вопросы к нему в лс!')
	await member.kick( reason = reason )
	await ctx.send( f'kick user { member.mention }')


@kick.error
async def kick_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды kick!')

@client.command( pass_context = True )
@commands.has_permissions( administrator = True)


async def ban ( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 2 )
	await member.send( f'Вас забанил { ctx.author.mention } по неизвестной мне причине все вопросы к нему в лс!')
	await member.ban( reason = reason )
	await ctx.send( f'ban user { member.mention }')


@ban.error
async def ban_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.author.send( f' { ctx.author.mention } необходимо ввести аргумент!')

	if isinstance( error, commands.MissingPermissions ):
		await ctx.author.send( f' { ctx.author.mention } у вам недостаточно прав для выполнения даной команды ban!')


token = open( 'token.txt', 'r' ).readline()

client.run( token )
