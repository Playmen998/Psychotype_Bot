import sqlite3 as sq
from create_bot import bot
import json


async def db_start():
    global db, cur

    db = sq.connect(r'BaseData/Psychotype_Test.db')
    cur = db.cursor()
    if db:
        print('Psychotype_Test connected OK!')
    cur.execute('CREATE TABLE IF NOT EXISTS Psychotype_Test(id INTEGER,question TEXT, answer TEXT)')
    empty_db = cur.execute("""select * from Psychotype_Test""").fetchall()
    if not empty_db:
        with open(r'Table/questionnaire_schema.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for i in range(60):
            cur.execute("INSERT INTO Psychotype_Test VALUES(?, ?, ?)",
                        (i, data[i]['text'][0]['value'], data[i]['answers'][0]['text'][0]['value']))
            cur.execute("INSERT INTO Psychotype_Test VALUES(?, ?, ?)",
                        (i, data[i]['text'][0]['value'], data[i]['answers'][1]['text'][0]['value']))
        db.commit()



async def get_question(i):
    quest = cur.execute(f"""select question from Psychotype_Test 
                    where id = {i} 
                    limit 1""").fetchone()
    return quest[0]

async def get_answer(i):
    answ = []
    for ret in cur.execute(f"""select answer from Psychotype_Test 
                    where id = {i} 
                    limit 2""").fetchall():
        answ.append(ret)
    return answ

