import sqlite3 as sq
import re


async def db_start():
    global db, cur

    db = sq.connect(r'BaseData/User_Answer.db')
    cur = db.cursor()
    if db:
        print('User_Answer connected OK!')

    string = ""
    for i in range(1, 61):
        string += f", q{i} TEXT"


    cur.execute(f'CREATE TABLE IF NOT EXISTS User_Answer(user_id INTEGER PRIMARY KEY, num INTEGER{string}, psychotype TEXT)')
    db.commit()

async def insert(dict_base):

    if cur.execute(f"""SELECT * FROM User_Answer
                WHERE user_id = {dict_base['user_id']}
                """).fetchone() is None: # нет человека в БД

        string_request = ", ?" * 62

        list_values = list(dict_base.values())
        while len(list_values) < 63:
            list_values.append(None)

        cur.execute(f"INSERT INTO User_Answer VALUES(?{string_request})", list_values)
        db.commit()
    else:
        record_user_values = cur.execute(f"""
            SELECT * from User_Answer
            where user_id = {dict_base['user_id']}
            """).fetchall()[0]


        new_answer_user = list(dict_base.values()) # передаются значения словаря (ответы пользователя)
        record_user_values = list(record_user_values) # ответы пользователя из БД

        """Тестируем замену данных"""

        if len(list(dict_base.keys())) == 2:
            return
        n = int(re.sub('[\D]', '', list(dict_base.keys())[2])) + 1

        record_user_values[1] = new_answer_user[1] # заменяем кол-во ответов
        final_answer_user = []
        for i in range(n): # n - макс 60
            if not record_user_values[i] is None:
                final_answer_user.append(record_user_values[i])
        final_answer_user = final_answer_user + new_answer_user[2:]

        string_request = ", ?" * 62

        while len(final_answer_user) < 63:
            final_answer_user.append(None)
        cur.execute(f"""DELETE from User_Answer where user_id = {final_answer_user[0]}""")
        db.commit()
        cur.execute(f"INSERT INTO User_Answer VALUES(?{string_request})", final_answer_user)
        db.commit()


async def select_num(user):
    return cur.execute(f"""
    SELECT * from User_Answer
    where user_id = {user}
    """).fetchall()[0][1]

async def select_data(user):
    return cur.execute(f"""
        SELECT * from User_Answer
        where user_id = {user}
        """).fetchall()[0]

async def safe_psychotype(user, psychotype):
    cur.execute(f"UPDATE User_Answer SET psychotype = '{psychotype}' WHERE user_id = {user}")
    db.commit()

async def delet(user):
    cur.execute(f"""DELETE from User_Answer where user_id = {user}""")
    db.commit()