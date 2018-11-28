from psycopg2 import sql
from db import Db

class User(object):
    @staticmethod 
    def create(data):
        query = sql.SQL("""INSERT INTO  users (first_name, middle_name, last_name, email, password)
        VALUES ({first_name}, {middle_name}, {last_name}, {email}, {password})
        RETURNING * """).format(
            first_name = sql.Literal(data.get('first_name')),
            middle_name = sql.Literal(data.get('middle_name')),
            last_name = sql.Literal(data.get('last_name')),
            email = sql.Literal(data.get('email')),
            password = sql.Literal(data.get('password'))
        )
        return Db.exec_query(query, returning = True)
    
    @staticmethod
    def update(user_id, data):
        query = sql.SQL("""UPDATE users SET 
                        first_name = {first_name},
                        middle_name = {middle_name},
                        last_name = {last_name},
                        email = {email}
            WHERE user_id = {user_id}
            RETURNING * """).format(
                first_name = sql.Literal(data.get('first_name')),
                middle_name = sql.Literal(data.get('middle_name')),
                last_name = sql.Literal(data.get('last_name')),
                email = sql.Literal(data.get('email')),
                user_id =  sql.Literal(user_id)
            )
        return Db.exec_query(query, returning = True)

    @staticmethod
    def find_by_id(id):
        query = sql.SQL("""
            SELECT * FROM users WHERE user_id = {id}""").format(id = sql.Literal(id))
        return Db.exec_query(query, returning=True)

    @staticmethod
    def query():
        query = sql.SQL("""
        SELECT * FROM users""")
        return Db.exec_query(query, returning_multi=True)

    @staticmethod
    def remove(user_id):
        query = sql.SQL("""
        DELETE FROM users WHERE user_id = {user_id}
        RETURNING * """).format(
            user_id = sql.Literal(user_id)
        )
        return Db.exec_query(query, returning = True)  