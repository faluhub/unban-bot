import json
from mysql import connector
from mysql.connector.abstracts import MySQLCursorAbstract
from Unban.secrets import Database

tables = [ # Copy sql code from workbench and just put it in strings.
    "CREATE TABLE `unban_bot`.`recent_messages` (`guildid` BIGINT NOT NULL, `userid` BIGINT NOT NULL, `messages` JSON NULL, PRIMARY KEY (`guildid`, `userid`), UNIQUE INDEX `guildid_UNIQUE` (`guildid` ASC) VISIBLE, UNIQUE INDEX `userid_UNIQUE` (`userid` ASC) VISIBLE)"
]

class Result:
    def __init__(self, cursor: MySQLCursorAbstract):
        self._cur  = cursor
        self.rows  = cursor.rowcount
    
    @property
    def value(self):
        fetch = self._cur.fetchone()

        if not fetch == None: return json.loads(fetch[0])
        else: return None

def connect():
    try: return (connector.connect(
                        host       =Database.HOST,
                        port       =Database.PORT,
                        db         =Database.SCHEMA,
                        user       =Database.USER,
                        passwd     =Database.PASSWORD,
                        charset    ="utf8mb4",
                        use_unicode=True
                    )
                )
    except Exception as e: (print("Couldn't connect to DB: "          + str(e)), quit())

def cursor(db):
    try: return db.cursor(buffered=True)
    except Exception as e: (print("Couldn't connect to DB's cursor: " + str(e)), quit())

def _create_tables():
    db  = connect()
    cur = cursor(db)

    print("Creating tables:")
    
    for i in tables:
        try: (cur.execute(i), db.commit(), print("  " + i.split("`")[3]))
        except Exception as e: print("  Error creating table '" + i.split("`")[3] + "': " + str(e))
    print("\n")

    cur.close()
    del cur

def select(q):
    db  = connect()
    cur = cursor(db)

    cur.execute(q)
    return Result(cur)

def delete(table, guildid):
    db  = connect()
    cur = cursor(db)

    cur.execute(f"DELETE FROM `{table}` WHERE guildid = `{guildid}`")
    db.commit()
    cur.close()
    del cur

def update(q):
    db  = connect()
    cur = cursor(db)

    cur.execute(q)
    db.commit()
    cur.close()
    del cur
