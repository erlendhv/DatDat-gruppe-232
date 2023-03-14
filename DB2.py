# New file
import sqlite3
con = sqlite3.connect('232DB.db')
cursor = con.cursor()

# stasjon = input("Skriv inn stasjon: ")
dag = input("Skriv inn dag: ")

cursor.execute("SELECT * FROM TogruteForekomst WHERE Ukedag = ?", (dag,))
forekomster = cursor.fetchall()
print(forekomster)

con.close()
