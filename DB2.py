# New file
import sqlite3
con = sqlite3.connect('232DB.db')
cursor = con.cursor()

# stasjon = input("Skriv inn stasjon: ")
dag = input("Skriv inn dag: ")

cursor.execute("SELECT * FROM TogruteForekomst WHERE Ukedag = ?", (dag,))
forekomster = cursor.fetchall()
print(forekomster)




Kundenummer = int(input("Skriv inn Kundenummer: "))
Kundenavn = input("Skriv inn navnet ditt: ")
Epost = input("Skriv inn E-post: ")
Mobilnummer = input("Skriv inn mobilnummer: ")

cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''', (Kundenummer, Kundenavn, Epost, Mobilnummer))


con.commit()

con.close()