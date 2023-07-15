from config import *
from models import *

@app.route('/api/web/', defaults={'path': ''})
@app.route('/api/web/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def api_web(path):
    v_apiurlsplit = [api_urlsplit(path, i) for i in range(10)]

    try:
        if request.method in ['GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']:
            return json.dumps({'success': False, 'code': 'H405', 'msg': 'Method not allowed.'}), 405

        _requestform = request.form
        _getlanguage = api_getlanguage()
        datetime_now = datetime.now()
        date_now = datetime_now.date()

        _language = _getlanguage['language']
        _translations = _getlanguage['translations']

        if v_apiurlsplit[0] == 'widget':
            if v_apiurlsplit[1] == 'home' and not v_apiurlsplit[2]:
                v_db_information_trending_movies = db_information.get(option = 'one', by = 'id', information_id = 'trending_movies')
                trending_movies_data = v_db_information_trending_movies['data']

                #TRENDING MOVIES
                trending_movies = []                
                for movie_id in trending_movies_data:
                    db_movie = db_movies.get(option = 'one', by = 'tmdb_id,language_id', tmdb_id = movie_id , language_id = _language)
                    if db_movie:
                        db_movie['url'] = f'{db_movie["_id"]}-{api_formaturl(db_movie["title"])}' 
                        trending_movies.append(db_movie)
                #TRENDING MOVIES END

                banner_trending_movies = trending_movies.copy() 
                random.shuffle(banner_trending_movies)
                
                return json.dumps({'success': True, 'html': render_template('home.html', banner_trending_movies = banner_trending_movies[:5], trending_movies = trending_movies)})
            
            elif v_apiurlsplit[1] == 'movie' and not v_apiurlsplit[3]:            
                movie_id = v_apiurlsplit[2][0:8]
                if movie_id.isnumeric():
                    movie_id = int(movie_id)
                    db_movie = db_movies.get(option = 'one', by = 'movie_id,language_id', movie_id = movie_id , language_id = _language)
                    if db_movie:
                        genres_ids = db_movie['genres']
                        genres = []
                        for genre_id in genres_ids:
                            db_genre = db_genres.get(option = 'one', by = 'genre_id', genre_id = genre_id)
                            genre = {
                                "id": genre_id,
                                "name": db_genre['name']
                            }
                            genres.append(genre)
                        
                        minutes = db_movie['runtime']
                        runtime_formated = "{:d}h {:02d}m".format((minutes // 60), (minutes % 60 ))
                        db_movie['runtime_formated'] = runtime_formated
                        db_movie['release_date_year'] = str(datetime.strptime(db_movie['release_date'], '%Y-%m-%d').year)

                        return json.dumps({'success': True, 'html': render_template('movie.html', db_movie = db_movie, genres = genres)})

        elif v_apiurlsplit[0] == 'data':
            if v_apiurlsplit[1] == 'change':
                if v_apiurlsplit[2] == 'language' and not v_apiurlsplit[3]:
                    language = _requestform.get('language')
                    if not language:
                        return json.dumps({'success': False, 'msg': _translations.get('empty_language', 'Language is empty! Please correct it and try again.')}) 
                    elif not language in ['en-us', 'es-mx']:
                        return json.dumps({'success': False, 'msg': _translations.get('invalid_language', 'Language is invalid! Please correct it and try again.')}) 
                    
                    session['language'] = language
                    return json.dumps({'success': True}) 
                
        return json.dumps({'success': False, 'code': f'H404', 'msg': 'Page not found.'}), 404
    except Exception as e:        
        api_savefile(os.path.join(app.root_path, 'log', 'api-web.txt'), f'[C{sys.exc_info()[-1].tb_lineno}] {e}')
        return json.dumps({'success': False, 'code': f'H500C{sys.exc_info()[-1].tb_lineno}', 'msg': 'An error occurred! The error was reported correctly and we will be working to fix it.'}), 500

@app.route('/api/web/token/csrf', methods = ['GET'])
@csrf.exempt
def api_web_token():
    return json.dumps({'success': True, 'token':  generate_csrf()}), 200