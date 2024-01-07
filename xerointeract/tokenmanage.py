import pymysql
from os import environ, path

from dotenv import load_dotenv
from settings import basedir
load_dotenv(path.join(basedir, '.env'))

class MySQLaccess:
    def __enter__(self):
        self.connection = pymysql.connect(
            host=environ.get('credhost'),
            user=environ.get('creduser'),
            password=environ.get('credpassword'),
            database=environ.get('creddatabase'))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection and self.connection.open:
            self.connection.close()

    def database_interact(self, query, parameters=None, return_result=False):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                if return_result:
                    result = cursor.fetchone()
                    return result
        except Exception as e:
            print(f"Error in database interaction: {e}")
        return None

    def get_token(self):
        query = "select * from tokens LIMIT 1;"
        result = self.database_interact(query, return_result=True)
        return result[1] if result else None

    def post_token(self, token):
        query = f"UPDATE tokens SET val = '{token}' WHERE id = 0;"
        self.database_interact(query)