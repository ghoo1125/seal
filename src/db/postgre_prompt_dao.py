import json
import os

import psycopg2


class PromptDao():
    TABLE_NAME = 'prompt'

    def __init__(self):
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if (DATABASE_URL is None):  # local
            DATABASE_URL = os.popen(
                'heroku config:get DATABASE_URL -a seal-line-messaging').read()[:-1]
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()

    def savePrompt(self, prompt):
        table_columns = '(user_id, hints)'
        postgres_insert_query = f'''
            INSERT INTO {PromptDao.TABLE_NAME} {table_columns} VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE
                SET hints = excluded.hints;
        '''
        user_id = prompt["user_id"]
        hints_json = json.dumps(prompt["hints"])
        record = (user_id, hints_json)
        self.cursor.execute(postgres_insert_query, record)
        self.conn.commit()

    def getPromptByUser(self, user_id):
        self.cursor.execute(
            f"SELECT user_id, hints FROM {PromptDao.TABLE_NAME} WHERE user_id = '{user_id}'")
        self.conn.commit()
        prompt = self.cursor.fetchone()
        if prompt is None:
            return {"user_id": user_id, "hints": []}
        else:
            v1, v2 = prompt
            return {"user_id": v1,  "hints": json.loads(v2)}

    def deletePromptByUser(self, user_id):
        self.cursor.execute(
            f"DELETE FROM {PromptDao.TABLE_NAME} WHERE user_id = '{user_id}'")
        self.conn.commit()
