from psycopg2 import connect, sql, extras
class Db(object):
    connecton = None
    @staticmethod
    def connect(config):
        Db.conn = connect(**config)
        return Db.conn
    
    @staticmethod
    def rollback():
        Db.conn.rollback()
    
    @staticmethod
    def commit():
        Db.conn.commit()

    @staticmethod
    def close():
        Db.conn.close()
    
    @staticmethod
    def get_cursor():
        return Db.conn.cursor(cursor_factory=extras.DictCursor)
    
    @staticmethod
    def exec_query(query, returning = False, returning_multi = False):
        cursor = None
        result = None
        try:
            cursor = Db.get_cursor()
            cursor.execute(query)
            if returning:
                result = cursor.fetchone()
            elif returning_multi:
                result = cursor.fetchall()
        except Exception as e:
            Db.rollback()
            print("Error executing query")
            print(e)
            raise e
        else:
            Db.commit()    
        finally:
            if cursor != None:
                cursor.close()
            return result
    