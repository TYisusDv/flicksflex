from config import *
from models import *
from api_web import *
scheduler = BackgroundScheduler()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods = ['GET'])
def web_main(path):    
    try:         
        languages = db_languages.get(option = 'all')
        
        return render_template('index.html', languages = languages)
    except Exception as e:
        api_savefile(os.path.join(app.root_path, 'log', 'web.txt'), f'[C{sys.exc_info()[-1].tb_lineno}] {e}')
        return json.dumps({'success': False, 'code': f'H500C{sys.exc_info()[-1].tb_lineno}', 'msg': 'An error occurred! The error was reported correctly and we will be working to fix it.'}), 500

@app.before_request
def web_languages():
    pass
    #v_language = api_getlanguage()
    #language = v_language['language']
    #translations = v_language['translations']
    
@app.context_processor
def web_inject():
    v_language = api_getlanguage()
    #language = v_language['language']
    translations = v_language['translations']
    return dict(translations=translations)

def task_onemin():
    with app.app_context(): 
        try:
            web_task_trending()
            web_task_translations()
        except Exception as e:
            api_savefile(os.path.join(app.root_path, 'log', 'task-onemin.txt'), f'[C{sys.exc_info()[-1].tb_lineno}] {e}')

def web_task_trending():   
    datetime_now = datetime.now()
    date_now = datetime_now.date()

    db_trending_movies = db_information.get(option = 'one', by = 'id', information_id = 'trending_movies')
    db_trending_movies_regdate = datetime.strptime(db_trending_movies['regdate'], '%Y-%m-%d').date()
    if (date_now - db_trending_movies_regdate).days > 7:
        tmdb_ids = []

        tmdb_trending_movies = api_gettmdb(url = f'/trending/movie/week?language=en-US').json()['results']
        for tmdb_movie in tmdb_trending_movies:
            tmdb_ids.append(tmdb_movie['id'])

        for tmdb_id in tmdb_ids:                    
            _db_movies = db_movies.get(option = 'one', by = 'tmdb_id', tmdb_id = tmdb_id)
            if not _db_movies:
                tmdb_movie = api_gettmdb(url = f'/movie/{tmdb_id}?language=en-US').json()
                uniqueid = int(api_uniqueid())
                
                genres_ids = []
                for genre in tmdb_movie['genres']:
                    db_genres.insert(genre_id = genre['id'], name = genre['name'])      
                    genres_ids.append(genre['id'])                 

                db_movies.insert(movie_id = uniqueid, title = tmdb_movie['title'], overview = tmdb_movie['overview'], runtime = tmdb_movie['runtime'], release_date = tmdb_movie['release_date'], tmdb_id = tmdb_id, genres = genres_ids)                

                api_saveimg(f'https://image.tmdb.org/t/p/original{tmdb_movie["poster_path"]}', os.path.join(app.root_path, 'static', 'img', 'movie', 'poster', 'en-us', f'{tmdb_id}.webp'), 85, 800)
                api_saveimg(f'https://image.tmdb.org/t/p/original{tmdb_movie["backdrop_path"]}', os.path.join(app.root_path, 'static', 'img', 'movie', 'backdrop', f'{tmdb_id}.webp'), 85, 1080)                    

        db_information.update(information_id = 'trending_movies', data = tmdb_ids, regdate = str(date_now))

def web_task_translations(): 
    language_id_list = ['es-mx']

    _db_movies = db_movies.get(option = 'all')
    for _db_movie in _db_movies:
        for language_id in language_id_list:
            _db_movie_id = _db_movie['_id']

            _db_movie_translations = db_movie_translations.get(option = 'one', by = 'movie_id,language_id', movie_id = _db_movie_id, language_id = language_id)
            if not _db_movie_translations:
                tmdb_id = _db_movie['tmdb_id']
                tmdb_movie = api_gettmdb(url = f'/movie/{tmdb_id}?language={language_id}').json()
                title = tmdb_movie['title']
                overview = tmdb_movie['overview']

                db_movie_translations.insert(movie_id = _db_movie_id, language_id = language_id, title = title, overview = overview)    
                api_saveimg(f'https://image.tmdb.org/t/p/original{tmdb_movie["poster_path"]}', os.path.join(app.root_path, 'static', 'img', 'movie', 'poster', language_id, f'{tmdb_id}.webp'), 85, 800)

scheduler.add_job(task_onemin, 'interval', minutes=1) #seconds=10 #minutes=1
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = app_debug)