from config import *
from models import *
from api_web import *

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods = ['GET'])
def web_main(path):    
    try:         
        languages = db_languages().get('all')
        return render_template('index.html', languages = languages)
    except Exception as e:
        api_savefile('log/web.txt', f'[C{sys.exc_info()[-1].tb_lineno}] {e}')
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
            v_datetime_now = datetime.now()
            v_date_now = v_datetime_now.date()

            trending_movies = db_information().get(option = 'one', by = 'id', information_id = 'trending_movies')
            if (v_date_now - trending_movies['regdate']).days > 7:
                tmdb_ids = []

                tmdb_trending_movies = api_gettmdb(url = f'/trending/movie/week?language=en-US').json()['results']
                for movie in tmdb_trending_movies:
                    tmdb_ids.append(movie['id'])

                for tmdb_id in tmdb_ids:                    
                    v_db_movies = db_movies().get(option = 'one', by = 'tmdb_id', tmdb_id = tmdb_id)
                    if not v_db_movies:
                        movie = api_gettmdb(url = f'/movie/{tmdb_id}?language=en-US').json()
                        uniqueid = api_uniqueid()

                        api_saveimg(f'https://image.tmdb.org/t/p/original{movie["poster_path"]}', f'static/img/movie/poster/en-us/{movie["id"]}.webp', 85, 800)
                        api_saveimg(f'https://image.tmdb.org/t/p/original{movie["backdrop_path"]}', f'static/img/movie/backdrop/en-us/{movie["id"]}.webp', 85, 1080)

                        db_movies().insert(movie_id = uniqueid, title = movie['title'], overview = movie['overview'], runtime = movie['runtime'], release_date = movie['release_date'], tmdb_id = tmdb_id)

                        for genre in movie['genres']:
                            db_genres().insert(genre_id = genre['id'], name = genre['name'])
                            db_movies_genres().insert(movie_id = uniqueid, genre_id = genre['id'])                        

                db_information().update(information_id = 'trending_movies', data = str(tmdb_ids), regdate = v_date_now)
        except Exception as e:
            api_savefile('log/task-onemin.txt', f'[C{sys.exc_info()[-1].tb_lineno}] {e}')

scheduler = BackgroundScheduler()
scheduler.add_job(task_onemin, 'interval', minutes=1) #seconds=10 #minutes=1
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = app_debug)