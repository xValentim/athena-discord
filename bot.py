import discord
from discord.ext import commands
from utils import *

import nest_asyncio
import os
nest_asyncio.apply()
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

type_messages = ['web', 'youtube']

def get_metadata_from_message(message):
    return {
        'message_id': message.id,
        'channel': message.channel,
        'author': message.author,
        'content': message.content,
    }
    
@commands.command()
async def get_summary(ctx, *args):
    arguments = ', '.join(args)
    
    message_id = ctx.message.id
    author = ctx.message.author
    channel = ctx.message.channel
    content = ctx.message.content
    
    username = author.name
    type_content = args[0]
    url = args[1]
    
    if type_content not in type_messages:
        await ctx.send(f'Por favor, informe o tipo de conteúdo que deseja resumir. Opções: {type_messages}')
        await ctx.send(f'Exemplo: $get_summary web https://www.uol.com.br')
        return
    await ctx.send(f'Processando o link...')
    
    input_tuple = (url, type_content, username)
    
    try:
        obj = await get_metadata(input_tuple[0], input_tuple[1], input_tuple[2])
        insert_objects([obj])
        await ctx.send('Conteúdo salvo no DB!')
        
    except Exception as e:
        print(e)
        await ctx.send(f'Erro ao acessar a página {url}')
        return
    
@commands.command()
async def generate_newsletter(ctx):
    await ctx.send('Gerando newsletter...')
    newsletter = create_newsletter(k=4)
    await ctx.send('Newsletter gerada!')
    await ctx.send(newsletter[:1_800])

bot.add_command(generate_newsletter)
bot.add_command(get_summary)
bot.run(TOKEN)