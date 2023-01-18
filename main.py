import disnake, time, asyncio
from disnake.ext import commands
import requests
import cloudscraper
import json
from xl import *

global history
global internal_id
global botname
global botid

token = "디스코드 토큰입력"
token2 = "CAI력토큰입력"

bot = commands.Bot(
    command_prefix='!',
    # test_guilds=[975696347506311168],
    # In the list above you can specify the IDs of your test guilds.
    # Why is this kwarg called test_guilds? This is because you're not meant to use
    # local registration in production, since you may exceed the rate limits.
)
scraper = cloudscraper.create_scraper()

@bot.slash_command(description="봇을 세팅합니다. Set up bot.")
async def set(inter: disnake.ApplicationCommandInteraction, bot_id: str):
    data = {"character_external_id":bot_id}
    url = "https://beta.character.ai/chat/history/create/"
    headers = {'authorization':token2}
    response = scraper.post(url, data=data, headers=headers)
    jsontext = json.loads(response.text)
    print(jsontext)
    if not jsontext['participants'][0]['is_human']:
        
        history = jsontext['external_id']
        
        internal_id = jsontext['participants'][0]['user']['username']
        
        botname = jsontext['participants'][0]['name']
        await inter.response.send_message("```세팅된 봇의 아이디: " + bot_id + "\n세팅된 봇의 대화 아이디: " + history + "\n세팅된 봇의 내부 아이디: " + internal_id + "\n세팅된 봇의 이름: " + botname  + "```\n" + "bot: " + jsontext['messages'][0]['text'])
        
        botid = bot_id
        set1(inter.user.name, inter.user.id)
        set2(botid, history)
        set3(internal_id, botname)
    elif jsontext['participants'][0]['is_human']:
        history = jsontext['external_id']
        internal_id = jsontext['participants'][1]['user']['username']
        botname = jsontext['participants'][1]['name']
        await inter.response.send_message("```세팅된 봇의 아이디: " + bot_id + "\n세팅된 봇의 대화 아이디: " + history + "\n세팅된 봇의 내부 아이디: " + internal_id + "\n세팅된 봇의 이름: " + botname  + "```\n" + "bot: " + jsontext['messages'][0]['text'])
        botid = bot_id
        set1(inter.user.name, inter.user.id)
        set2(botid, history)
        set3(internal_id, botname)
        
    

@bot.slash_command(description="봇과 대화합니다. Talk to the bot.")
async def chat(inter: disnake.ApplicationCommandInteraction, chat: str):
    try:
        userExistance, userRow = checkUser(inter.user.name, inter.user.id)
        if userExistance:
            _botid, _history, _internal, _bot_name = userInfo(userRow)
            data = {'history_external_id':_history, 'character_external_id':_botid, 'text':chat, 'tgt':_internal}
            url = "https://beta.character.ai/chat/streaming/"
            headers = {'authorization':token2}
            await inter.response.send_message("응답 대기 중...\n오랜 시간이 소요될 수 있습니다.")
            response = scraper.post(url, data=data, headers=headers)
            print(response.text)
            jsontext = json.loads(response.text.split('"last_user_msg_id":')[0]+'"last_user_msg_id": 0}')
            await inter.edit_original_response(inter.user.name + ": " + chat + "\n" + _bot_name + ': ' + jsontext['replies'][0]['text'])
    except:
        await inter.edit_original_response("오류가 발생했습니다. 봇 세팅 여부를 확인해주세요.")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")

bot.run(token)
