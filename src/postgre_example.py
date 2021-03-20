import json
import os

import psycopg2

if __name__ == "__main__":
    # --- Connect db ---
    # DATABASE_URL = os.environ.get('DATABASE_URL') # online
    # if (DATABASE_URL is None): # local
    #     DATABASE_URL = os.popen(
    #         'heroku config:get DATABASE_URL -a seal-line-messaging').read()[:-1]
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # cursor = conn.cursor()

    # --- Upsert row ---
    # table_columns = '(user_id, hints)'
    # postgres_insert_query = f'''
    #     INSERT INTO prompt {table_columns} VALUES (%s, %s)
    #     ON CONFLICT (user_id) DO UPDATE
    #         SET hints = excluded.hints;
    #     '''
    # user_id = "Louis"
    # hints_json = json.dumps([{"question": "abc", "answer": 456}])
    # record = (user_id, hints_json)
    # cursor.execute(postgres_insert_query, record)
    # conn.commit()

    # --- Read records ---
    # cursor.execute("SELECT user_id, hints FROM prompt WHERE user_id = 'U3fb19078ee2d93ec2e2664948786bd65'")
    # conn.commit()
    # data = cursor.fetchall()
    # for row in data:
    #     print(row)

    # --- Delete record ---
    # cursor.execute("DELETE FROM prompt WHERE user_id = 'Louiss'")
    # conn.commit()

    # --- Create table ---
    # create_table_query = '''CREATE TABLE prompt(
    #     user_id TEXT UNIQUE NOT NULL,
    #     hints TEXT
    # );'''
    # cursor.execute(create_table_query)
    # conn.commit()

    # --- Drop table ---
    # drop_table_query = "DROP TABLE prompt"
    # cursor.execute(drop_table_query)
    # conn.commit()

    # --- Close connection ---
    # cursor.close()
    # conn.close()
