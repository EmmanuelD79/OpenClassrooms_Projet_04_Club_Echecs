from tinydb import TinyDB
from constants.database import DB_FILENAME, TABLE_NAME_TOURNAMENTS, TABLE_NAME_ACTORS


DB = TinyDB(DB_FILENAME)
ACTORS = DB.table(TABLE_NAME_ACTORS)
TOURNAMENTS = DB.table(TABLE_NAME_TOURNAMENTS)
