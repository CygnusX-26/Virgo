import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()

# c.execute("""CREATE TABLE users (
#             id integer,
#             guild integer,
#             exp integer       
#             )""")

#c.execute("INSERT INTO users VALUES (221731072822607872, 733554822480920596, 0)")

#c.execute("SELECT * FROM users WHERE id=221731072822607872")

#many, all
#print(c.fetchone())


conn.commit()

conn.close()