from config import *

class db_languages:
    def __init__(self):
        self._translations = api_getlanguage()['translations']
    
    def get(self, option = None):
        if option == 'one':
            cur = mysql.connection.cursor()
            cur.execute('SELECT us_users.*, mem_memberships.mem_name FROM us_users INNER JOIN mem_memberships ON mem_memberships.mem_id = us_users.mem_id WHERE us_users.us_id = %s',(us_id,))
            data = cur.fetchone()
            cur.close()
            return data
        elif option == 'all':
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM languages')
            data = cur.fetchall()
            cur.close()
            return data
        else:
            raise ValueError(self._translations.get('empty_option', 'Option is invalid! Please correct it and try again.'))
        
class db_information:
    def __init__(self):
        pass
    
    def get(self, option = None, by = None, information_id = None):
        if option == 'one':
            if by == 'id':
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM information WHERE id = %s', (information_id,))
                data = cur.fetchone()
                cur.close()
                return data
            return None
        elif option == 'all':
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM languages')
            data = cur.fetchall()
            cur.close()
            return data
        else:
            return None
    
    def update(self, information_id = None, data = None, regdate = None):
        cur = mysql.connection.cursor()        
        cur.execute('UPDATE information SET data = %s, regdate = %s WHERE id = %s', (data, regdate, information_id,))
        mysql.connection.commit()
        cur.close()     

        return True

class db_genres:
    def __init__(self):
        pass

    def insert(self, genre_id = None, name = None):
        cur = mysql.connection.cursor()        
        cur.execute('INSERT IGNORE INTO genres(id, name) VALUES(%s, %s)', (genre_id, name,))
        mysql.connection.commit()
        cur.close()     
        return True

class db_movies:
    def __init__(self):
        pass
    
    def get(self, option = None, by = None, movie_id = None, title = None, overview = None, tmdb_id = None):
        if option == 'one':
            if by == 'id':
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
                data = cur.fetchone()
                cur.close()
                return data
            elif by == 'tmdb_id':
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM movies WHERE tmdb_id = %s', (tmdb_id,))
                data = cur.fetchone()
                cur.close()
                return data
            return None
        elif option == 'all':
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM movies')
            data = cur.fetchall()
            cur.close()
            return data
        else:
            return None 
        
    def insert(self, movie_id = None, title = None, overview = None, runtime = None, release_date = None, tmdb_id = None):
        cur = mysql.connection.cursor()        
        cur.execute('INSERT IGNORE INTO movies(id, title, overview, runtime, release_date, tmdb_id) VALUES(%s, %s, %s, %s, %s, %s)', (movie_id, title, overview, runtime, release_date, tmdb_id,))
        mysql.connection.commit()
        cur.close()  
        return True

class db_movie_translations:
    def __init__(self):
        pass
    
    def get(self, option = None, by = None, movie_id = None, language_id = None):
        if option == 'one':
            if by == 'movie_id,language_id':
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM movie_translations WHERE movie_id = %s AND language_id = %s', (movie_id, language_id,))
                data = cur.fetchone()
                cur.close()
                return data
            return None
        else:
            return None 
        
    def insert(self, title = None, overview = None, movie_id = None, language_id = None):
        cur = mysql.connection.cursor()        
        cur.execute('INSERT IGNORE INTO movie_translations(title, overview, movie_id, language_id) VALUES(%s, %s, %s, %s)', (title, overview, movie_id, language_id,))
        mysql.connection.commit()
        cur.close()
        return True
    
class db_movies_genres:
    def __init__(self):
        pass

    def insert(self, movie_id = None, genre_id = None):
        cur = mysql.connection.cursor()        
        cur.execute('INSERT IGNORE INTO movies_genres(movie_id, genre_id) VALUES(%s, %s)', (movie_id, genre_id,))
        mysql.connection.commit()
        cur.close() 
        return True