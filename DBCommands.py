import sqlite3
class DBCommands:
    CREATE ="""CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE, buttons TEXT, message_id INTEGER)"""
    async def create(self):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.CREATE
            cursor.execute(command)

    ADD_USER = """INSERT INTO users (id) VALUES ($1)"""
    async def add_user(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.ADD_USER
            cursor.execute(command, chatid)

    UPDATE_BUTTONS = """UPDATE users SET buttons = $1 WHERE id = $2"""
    async def update_buttons(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_BUTTONS
            cursor.execute(command, par)

    UPDATE_MESSAGE_ID = """UPDATE users SET message_id = $1 WHERE id = $2"""
    async def update_message_id(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_MESSAGE_ID
            cursor.execute(command, par)\




    SELECT_MESSAGE_ID="""SELECT message_id FROM users WHERE id= $1"""
    async def select_message_id(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_MESSAGE_ID
            return cursor.execute(command, chatid)

    SELECT_BUTTONS = """SELECT buttons FROM users WHERE id= $1"""
    async def select_buttons(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_BUTTONS
            return cursor.execute(command, chatid)