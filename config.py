from flask import Flask, render_template, request, redirect, url_for, session, escape, make_response, send_file
from flask_wtf.csrf import CSRFProtect, generate_csrf
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from itsdangerous import URLSafeSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from unidecode import unidecode
from PIL import Image
from io import BytesIO
import json, uuid, requests, re, math, time, sys, random, shutil, os, base64, subprocess, psutil, glob, socket, string, html

app_local = False
app_hostname = socket.gethostname()

if app_hostname == "jesus-linux":
    app_local = True

if app_local:   
    app_db_db = 'flicksflex'
    app_link = 'http://127.0.0.1:5000'
    app_debug = True
else:    
    app_db_db = 'flicksflex'
    app_link = 'http://127.0.0.1:5000'
    app_debug = False

csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)
app.secret_key = "SeCrEt_G0cE3r8277"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # URL de Redis
app.config['result_backend'] = 'redis://localhost:6379/0'  # URL de Redis
db_mongoClient = MongoClient('mongodb://localhost:27017/')
db_mongo = db_mongoClient[app_db_db]


def api_verify_session():
    #0 = Not Logged
    #1 = Logged

    token = request.cookies.get('enigmatm')
    serializer = URLSafeSerializer(app.secret_key)
    
    try:
        data = serializer.loads(token)
        session["us_id"] = data['us_id']
        session["sess_id"] = data['sess_id']
    except:
        pass

    if "us_id" not in session:
        session.clear()
        return 0
    
    if "sess_id" not in session:
        session.clear()
        return 0
    
    return 1
    
def api_urlsplit(path, n):
    try:
        return path.split("/")[n] if len(path.split("/")) > n else None
    except:
        return None

def api_emailvalid(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

def api_savefile(name, text):
    try:
        with open(name, "a+") as f:
            f.write(f"{text}\n")
            f.close()
            
        return True
    except:
        return False

def api_hashbcrypt(passw):
    return bcrypt.hash(passw)

def api_verifybcrypt(passw, hash):
    return bcrypt.verify(passw, hash)

def api_genuniqueid():
    unique_id = str(uuid.uuid4().hex)[:16]
    return unique_id.upper()

def api_permissions(mem_id):
    #NORMAL
    listAccess = [173614]
    
    #ADMIN
    if mem_id == 109147:
        listAccess = [109147, 116995, 120996, 136721, 158272, 173614]

    #MOD
    if mem_id == 116995:
        listAccess = [116995, 120996, 136721, 158272, 173614]

    #SELLER
    if mem_id == 120996:
        listAccess = [120996, 136721, 158272, 173614]
    
    #TESTER
    if mem_id == 136721:
        listAccess = [136721, 158272, 173614]

    #PRO
    if mem_id == 158272:
        listAccess = [158272, 173614]

    return listAccess

def api_isFloat(num):
    try:
        float(num)
        return True
    except:
        return False
    
def api_isBoolean(num):
    try:
        bool(num)
        return True
    except:
        return False

def api_getlinefile(name):
    with open(name, 'r') as file:
        lines = file.readlines()

    line = random.choice(lines)

    return line.strip()
    
def api_getdevice(user_agent):
    regex = r'\((.*?)\)'
    match = re.search(regex, user_agent)
    if match:
        device_info = match.group(1)
        device_name = device_info.split(';')[0]
        try:
            device_name_1 = device_info.split(';')[1]
            device_name = f'{device_name_1}; {device_name}'
        except:
            pass
    else:
        device_name = 'Other'

    return device_name

def api_getlanguage():
    try:
        if not 'language' in session:
            browser_language = request.accept_languages[0][0]
            languages = {
                'es-419': 'es-mx',
            }
            language = languages.get(browser_language, 'en-us')
            session['language'] = language
    except:
        session['language'] = 'en-us'

    language = session['language']

    translations = {}
    with open(f'translations/{language}.json', 'r') as f:
        translations = json.load(f)
    
    response = {
        'language': language,
        'translations': translations
    }
    return response

def api_gettmdb(url = ''):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNGM4OTQ2MmU4NDcxOTA5YWI4ODc4YTgwY2I5N2ZlOSIsInN1YiI6IjY0Njk1MjM1MmJjZjY3MDE3MmIxNmIyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UpgcAx_FsG6SFvzEUxiU_PAzLgJzvseQZVV-RsduAUQ"
    }

    response = requests.get('https://api.themoviedb.org/3' + url, headers = headers)
    return response

def api_formaturl(text):
    formattedtext = unidecode(text) 
    formattedtext = formattedtext.replace("-", "") 
    formattedtext = formattedtext.replace("  ", "-")
    formattedtext = formattedtext.replace(" ", "-")
    formattedtext = re.sub(r"[^a-zA-Z0-9-]", "", formattedtext)    
    formattedtext = formattedtext[:100].lower()
    
    return formattedtext

def api_uniqueid():
    fact1 = str(uuid.uuid4().int)[:4]
    fact2 = str(random.randint(1000, 9999))
    uniqueid = fact1 + fact2
    return uniqueid

def api_saveimg(url, name, quality, new_height):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    new_width = int((width / height) * new_height)
    resized_img = img.resize((new_width, new_height))
    resized_img.save(name, 'WebP', quality = quality)
    return True
