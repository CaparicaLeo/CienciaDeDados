import sqlite3 as sqllite
import pandas as pd

con = sqllite.connect("mydata.sqlite")

con.execute(
    """
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
    """
)

con.execute("INSERT INTO test (id,nome) VALUES (1, 'Caparica')")
con.execute("INSERT INTO test (id,nome) VALUES (2, 'Milena')")

con.commit()

cursor = con.execute('SELECT * FROM test')
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])

print(df)
con.close()