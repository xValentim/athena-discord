from langchain.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable
import bs4
from operator import itemgetter
import markdown
import datetime
import pytube
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
URI = uri
collection = client[DB_NAME][COLLECTION_NAME]

def check_if_url_exists(url: str):
    item_details = collection.find({'url': url})
    for item in item_details:
        return True
    return False

def get_only_window_old_items(window: int, granularity: str):
    if granularity == 'hours':
        item_details = collection.find({'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(hours=window)}})
    elif granularity == 'days':
        item_details = collection.find({'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(days=window)}})
    elif granularity == 'minutes':
        item_details = collection.find({'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(minutes=window)}})
    else:
        return None
    items = []
    for item in item_details:
        items.append(item)
    return items

def format_object(url, content_type, original_content, summarization, who_added, date_added):
    return {
        'url': url,
        'content_type': content_type,
        'original_content': original_content,
        'summarization': summarization,
        'who_added': who_added,
        'date_added': date_added
    }
    
def count_items_per_user(username: str, window_time: int=10, granularity: str='minutes'):
    if granularity == 'hours':
        item_details = collection.find({'who_added': username, 
                                    'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(hours=window_time)}})
    elif granularity == 'days':
        item_details = collection.find({'who_added': username, 
                                    'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(days=10)}})
    elif granularity == 'minutes':
        item_details = collection.find({'who_added': username, 
                                    'date_added': {'$gte': datetime.datetime.now() - datetime.timedelta(minutes=window_time)}})
    count = 0
    for item in item_details:
        count += 1
    return count

async def get_metadata(url: str, content_type: str, username: str):
    
    if content_type == 'web':
        original_content = await web_loader(url)
        original_content_str = "\n".join([x.page_content for x in original_content])[:3_000]
        summarization = chain_summarization(original_content_str)
        return format_object(url, content_type, original_content_str, summarization, username, datetime.datetime.now())
    elif content_type == 'youtube':
        original_content_str, summarization = chain_youtube_summarization(url, size=4)
        return format_object(url, content_type, original_content_str, summarization, username, datetime.datetime.now())
    else:
        return None

def user_can_add_content(username: str, window_time: int=10, granularity: str='minutes', limit: int=5):
    return count_items_per_user(username, window_time, granularity) < limit
    
def insert_objects(objects, window_time: int=10, granularity: str='minutes'):
    for obj in objects:
        username = obj['who_added']
        url_exists = check_if_url_exists(obj['url'])
        user_can_add = user_can_add_content(username)
        if not url_exists and user_can_add:
            collection.insert_one(obj)
        else:
            if not user_can_add:
                print('User cannot add more content')
            if url_exists:
                print('URL already exists')
                
def format_text(x: dict):
    return f'URL: {x["url"]}\nTipo de conteúdo: {x["content_type"]}\nQuem adicionou: {x["who_added"]}\nData de adição: {x["date_added"]}\nConteudo resumido: {x["summarization"]}\n'                

def create_newsletter(k: int=-1):
    prepo_text = [format_text(x) for x in get_only_window_old_items(window=1, granularity='days')]
    if k == -1:
        all_content = "\n".join(prepo_text)
    else:
        all_content = "\n".join(prepo_text[:-k])
    
    messages = [
        ('system', 'Você é um assistente virtual que vai receber uma lista de conteúdos adicionados por alunos para que uma newsletter fosse criada. Sua tarefa é organizar esses conteúdos em uma newsletter, destacando os principais pontos de cada conteúdo e explicando-os de forma acessível. A ênfase deve ser na simplicidade, garantindo que o usuário compreenda todos os conceitos e informações chave. Ao fazer a newsletter, priorize a clareza, organização e a explicação de cada ponto central do conteúdo enviado.'), 
        ('user', 'aqui está o conteudo {all_content}')] 
    prompt = ChatPromptTemplate.from_messages(messages)
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
    chain = (
        {
            'all_content': itemgetter('all_content')
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({'all_content': all_content})


async def web_loader(url: str):
    loader = WebBaseLoader(web_paths=[url])
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs

def chain_summarization(content: str, size: str = 'medium'):
    
    if size == 'small':
        messages = [('system', 'Você é um assistente virtual com o objetivo de sumarizar textos de maneira clara, didática e objetiva. Sua tarefa é receber o conteúdo de uma página web e gerar uma sumarização curta que destaque os principais pontos, explicando-os de forma acessível. A ênfase deve ser na simplicidade, garantindo que o usuário compreenda todos os conceitos e informações chave. Ao fazer a sumarização, priorize a clareza, organização e a explicação de cada ponto central do conteúdo enviado.'), ('user', 'aqui está o conteudo {texto}')] 
    elif size == 'medium':
        messages = [('system', 'Você é um assistente virtual com o objetivo de sumarizar textos de maneira clara, didática e objetiva. Sua tarefa é receber o conteúdo de uma página web e gerar uma sumarização de tamanho médio que destaque os principais pontos, explicando-os de forma acessível. A ênfase deve ser na simplicidade, garantindo que o usuário compreenda todos os conceitos e informações chave. Ao fazer a sumarização, priorize a clareza, organização e a explicação de cada ponto central do conteúdo enviado.'), ('user', 'aqui está o conteudo {texto}')]
    elif size == 'large':
        messages = [('system', 'Você é um assistente virtual com o objetivo de sumarizar textos de maneira clara, didática e objetiva. Sua tarefa é receber o conteúdo de uma página web e gerar uma sumarização longa e detalhada que destaque os principais pontos, explicando-os de forma acessível. A ênfase deve ser na simplicidade, garantindo que o usuário compreenda todos os conceitos e informações chave. Ao fazer a sumarização, priorize a clareza, organização e a explicação de cada ponto central do conteúdo enviado.'), ('user', 'aqui está o conteudo {texto}.')]

    prompt = ChatPromptTemplate.from_messages(messages)
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
    chain = (
        {
            'texto': itemgetter('texto')
        }
        |prompt
        | llm
        |StrOutputParser()
    )

    resume = chain.invoke({'texto': content})
    return resume

def chain_youtube_summarization(url: str, size: str) -> Runnable:
    """ 
    Responsável por criar uma chain que irá sumarizar um vídeo do YouTube.

    Args:
        url (str): A URL do vídeo do YouTube.
        size (str): O tamanho de parágrafos para o resumo.

    Returns:
        Runnable: Um Runnable que executa a sumarização do vídeo do YouTube.

    Raises:
        HTTPException: Se houver um erro ao acessar o vídeo do YouTube.
    """
    
    try:
        video_id = url.find('v=')
        video_id = url[video_id+2:]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])

        texto = ""
        for line in transcript:
            texto += line['text'] + " "
    except Exception as e:
        return 'conteudo indisponivel'


    messages = [('system', 'Você é um assistente virtual com o objetivo de sumarizar vídeos de maneira clara, didática e objetiva. Sua tarefa é receber o conteúdo de um vídeo e gerar uma sumarização curta que destaque os principais pontos, explicando-os de forma acessível. A ênfase deve ser na simplicidade, garantindo que o usuário compreenda todos os conceitos e informações chave. Ao fazer a sumarização, priorize a clareza, organização e a explicação de cada ponto central do conteúdo enviado.'), 
    ('system', f'Utilize até, no MÁXIMO, {size} parágrafos para o resumo.'),
    ('user', f'aqui está o conteudo {texto}')] 

    
    prompt = ChatPromptTemplate.from_messages(messages)
    llm = ChatOpenAI(model = 'gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return texto, chain.invoke({})