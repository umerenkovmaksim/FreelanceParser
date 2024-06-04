import aiosqlite
from config import database
from utils import dict_factory


async def init_db():
    async with aiosqlite.connect(database) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                auto_habr BOOLEAN DEFAULT (FALSE),
                auto_freelance BOOLEAN DEFAULT (FALSE),
                auto_kwork BOOLEAN DEFAULT (FALSE),
                habr_categories TEXT DEFAULT [-1],
                freelance_categories TEXT DEFAULT [-1],
                kwork_categories TEXT DEFAULT [-1]
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS last_tasks (
                user_id INTEGER PRIMARY KEY,
                last_habr TEXT DEFAULT [default],
                last_freelance TEXT DEFAULT [default],
                last_kwork TEXT DEFAULT [default]         
            )
        ''')
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect(database) as db:
        await db.execute('''
            INSERT INTO users (user_id) VALUES (?)
        ''', (user_id,))
        await db.execute('''
            INSERT INTO last_tasks (user_id) VALUES (?)
        ''', (user_id,))
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(database) as db:
        async with db.execute('''
            SELECT user_id FROM users WHERE user_id = ?
        ''', (user_id,)) as cursor:
            user = await cursor.fetchone()
            return user if user else None
        
        
async def get_user_settings(user_id):
    async with aiosqlite.connect(database) as db:
        db.row_factory = dict_factory
        async with db.execute('''
            SELECT * FROM users WHERE user_id = ?
        ''', (user_id,)) as cursor:
            user_data = await cursor.fetchone()
            if dict(user_data):
                return dict(user_data)
            return None
            
            
async def set_user_settings(user_id, *args, **kwargs):
    async with aiosqlite.connect(database) as db:
        await db.execute(f'''
            UPDATE users SET {",".join(["%s = '%s'" % (elem, kwargs[elem]) for elem in kwargs])} WHERE user_id = ?
        ''', (
            user_id,
        ))
        await db.commit()


async def get_active_automode_users():
    async with aiosqlite.connect(database) as db:
        async with db.execute(
            '''SELECT * FROM users WHERE auto_habr = TRUE OR auto_freelance = TRUE OR auto_kwork = TRUE'''
        ) as cursor:
            return cursor.fetchall()
        

async def get_user_last_tasks(user_id):
    async with aiosqlite.connect(database) as db:
        db.row_factory = dict_factory
        async with db.execute(
            '''SELECT * FROM last_tasks WHERE user_id = ?''',
        (user_id,)) as cursor:
            last_tasks = await cursor.fetchone()
            if dict(last_tasks):
                return dict(last_tasks)
            return None
            

async def set_user_last_task(user_id, last_habr=None, last_freelance=None, last_kwork=None):
    last_tasks = await get_user_last_tasks(user_id)
    async with aiosqlite.connect(database) as db:
        await db.execute('''
            UPDATE last_tasks SET last_habr = ?, last_freelance = ?, last_kwork = ? WHERE user_id = ?
        ''', (
            last_habr if last_habr else last_tasks['last_habr'], 
            last_freelance if last_freelance else last_tasks['last_freelance'], 
            last_kwork if last_kwork else last_tasks['last_kwork'], 
            user_id,
        ))
        await db.commit()