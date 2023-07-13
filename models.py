from config import *

class db_languages:
    @staticmethod
    def get(option = None):
        if option == 'one':            
            return None
        elif option == 'all':
            data = db_mongo.languages.find()
            return data
        else:
            return None
        
class db_information:
    @staticmethod
    def get(option = None, by = None, information_id = None):
        if option == 'one':
            if by == 'id':
                data = db_mongo.information.find_one({"_id": information_id})
                return data
            
            return None
        elif option == 'all':            
            return None
        else:
            return None
        
    @staticmethod
    def update(information_id = None, data = None, regdate = None):
        query = {
            "_id": information_id
        }        
        update = {
            "data": data,
            "regdate": regdate
        }        
        data = db_mongo.information.update_one(query, {"$set": update})
        return None

class db_genres:
    @staticmethod
    def insert(genre_id = None, name = None):
        document = {
            "_id": genre_id,
            "name": name
        } 
        try: 
            data = db_mongo.genres.insert_one(document, bypass_document_validation=True)
            return data
        except DuplicateKeyError:
            pass
        
        return None        

class db_movies:
    @staticmethod    
    def get(option = None, by = None, movie_id = None, title = None, overview = None, tmdb_id = None):
        if option == 'one':
            if by == 'id':
                data = db_mongo.movies.find_one({"_id": movie_id})
                return data
            elif by == 'tmdb_id':
                data = db_mongo.movies.find_one({"tmdb_id": tmdb_id})
                return data
            return None
        elif option == 'all':
            data = db_mongo.movies.find()
            return data
        else:
            return None 
        
    @staticmethod  
    def insert(movie_id = None, title = None, overview = None, runtime = None, release_date = None, tmdb_id = None, genres = None):
        document = {
            "_id": movie_id,
            "title": title,
            "overview": overview,
            "runtime": runtime,
            "release_date": release_date,
            "tmdb_id": tmdb_id,
            "genres": genres
        }

        try: 
            data = db_mongo.movies.insert_one(document, bypass_document_validation=True)
            return data
        except DuplicateKeyError:
            pass
        
        return None

class db_movie_translations:
    @staticmethod
    def get(option = None, by = None, movie_id = None, language_id = None):
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
    
    @staticmethod 
    def insert(title = None, overview = None, movie_id = None, language_id = None):
        cur = mysql.connection.cursor()        
        cur.execute('INSERT IGNORE INTO movie_translations(title, overview, movie_id, language_id) VALUES(%s, %s, %s, %s)', (title, overview, movie_id, language_id,))
        mysql.connection.commit()
        cur.close()
        return True