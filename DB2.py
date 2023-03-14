# New file
import sqlite3
con = sqlite3.connect('232DB.db')
cursor = con.cursor()


# Brukerhistorie c
stasjon = input("Skriv inn stasjon: ")
dag = input("Skriv inn dag: ")

cursor.execute("select TogruteID from StasjonerITabell natural join (select * from Togrutetabell natural join (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?", (dag, stasjon))
forekomster = cursor.fetchall()
print(forekomster)


# Brukerhistorie e
Kundenummer = 0
cursor.execute("select Kundenummer from Kunde")
Kundenummer = cursor.fetchall()[-1][0]
Kundenummer += 1
Kundenavn = input("Skriv inn navnet ditt: ")
Epost = input("Skriv inn E-post: ")
Mobilnummer = input("Skriv inn mobilnummer: ")

cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''',
               (Kundenummer, Kundenavn, Epost, Mobilnummer))


con.commit()

con.close()
