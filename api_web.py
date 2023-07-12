from config import *
from models import *

@app.route('/api/web/', defaults={'path': ''})
@app.route('/api/web/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def api_web(path):
    v_apiurlsplit = [api_urlsplit(path, i) for i in range(10)]

    try:
        if request.method in ['GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']:
            return json.dumps({'success': False, 'code': 'H405', 'msg': 'Method not allowed.'}), 405

        v_requestform = request.form
        v_getlanguage = api_getlanguage()
        v_datetime_now = datetime.now()
        v_date_now = v_datetime_now.date()

        v_language = v_getlanguage['language']
        translations = v_getlanguage['translations']

        if v_apiurlsplit[0] == 'widget':
            if v_apiurlsplit[1] == 'home' and not v_apiurlsplit[2]:
                db_trending_movies = db_information().get(option = 'one', by = 'id', information_id = 'trending_movies')
                db_trending_movies_data = db_trending_movies['data']

                #TRENDING MOVIES
                trending_movies = []                
                for movie_id in eval(db_trending_movies_data):
                    movie = db_movies().get(option = 'one', by = 'tmdb_id', tmdb_id = movie_id)
                    if movie:
                        if v_language != 'en-us':
                            movie_translation = None
                            while True:
                                movie_translation = db_movie_translations().get(option = 'one', by = 'movie_id,language_id', movie_id = movie['id'], language_id = v_language)
                                if not movie_translation:
                                    db_movie_translations().insert(tmdb_id = movie_id, movie_id = movie['id'], language_id = v_language)
                                else:                                    
                                    break
                                  
                            movie['title'] = movie_translation['title']
                            movie['overview'] = movie_translation['overview']
                        
                        movie['url'] = f'{movie["id"]}-{api_formaturl(movie["title"])}' 
                        trending_movies.append(movie)
                #TRENDING MOVIES END

                banner_trending_movies = trending_movies.copy() 
                random.shuffle(banner_trending_movies)
                
                return json.dumps({'success': True, 'html': render_template('home.html', banner_trending_movies = banner_trending_movies[:5], trending_movies = trending_movies)})
        
        elif v_apiurlsplit[0] == 'data':
            if v_apiurlsplit[1] == 'change':
                if v_apiurlsplit[2] == 'language' and not v_apiurlsplit[3]:
                    language = v_requestform.get('language')
                    if not language:
                        return json.dumps({'success': False, 'msg': translations.get('empty_language', 'Language is empty! Please correct it and try again.')}) 
                    elif not language in ['en-us', 'es-mx']:
                        return json.dumps({'success': False, 'msg': translations.get('invalid_language', 'Language is invalid! Please correct it and try again.')}) 
                    
                    session['language'] = language
                    return json.dumps({'success': True}) 

    except Exception as e:
        api_savefile('log/api-web.txt', f'[C{sys.exc_info()[-1].tb_lineno}] {e}')
        return json.dumps({'success': False, 'code': f'H500C{sys.exc_info()[-1].tb_lineno}', 'msg': 'An error occurred! The error was reported correctly and we will be working to fix it.'}), 500

@app.route('/api/web/token/csrf', methods = ['GET'])
@csrf.exempt
def api_web_token():
    return json.dumps({'success': True, 'token':  generate_csrf()}), 200