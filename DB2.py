# New file
import sqlite3, datetime
con = sqlite3.connect('232DB.db')
cursor = con.cursor()

<<<<<<< HEAD
# stasjon = input("Skriv inn stasjon: ")
# dag = input("Skriv inn dag: ")

# cursor.execute("SELECT * FROM TogruteForekomst WHERE Ukedag = ?", (dag,))
# forekomster = cursor.fetchall()
# print(forekomster)


startStasjon = input("Skriv inn ønsket startstasjon: ")
sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
year, month, day = map(int, dato_str.split("-"))
dato1 = datetime.date(year, month, day)
dato2 = dato1 + datetime.timedelta(days=1)
klokkeslett = input("Angi ønsket klokkeslett: ")

ukedag1 = dato1.strftime("%A")
ukedag2 = dato2.strftime("%A")

cursor.execute("SELECT TogruteID FROM (TogruteForekomst JOIN (StasjonerITabell AS st JOIN Togrutetabell AS tt \
ON st.TogruteTabellID = tt.TogruteTabellID) ON  WHERE Ukedag = ? OR Ukedag = ? AND Startstasjon = ? AND Sluttstasjon = ? \
AND Avgangstid >= ?", (ukedag1), (ukedag2), (startStasjon), (sluttStasjon), (klokkeslett))


# Kundenummer = int(input("Skriv inn Kundenummer: "))
# Kundenavn = input("Skriv inn navnet ditt: ")
# Epost = input("Skriv inn E-post: ")
# Mobilnummer = input("Skriv inn mobilnummer: ")

# cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''', (Kundenummer, Kundenavn, Epost, Mobilnummer))
=======

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
>>>>>>> 9ce725020b12d671388353d1a74127a881638978


con.commit()

con.close()
<<<<<<< HEAD


=======
>>>>>>> 9ce725020b12d671388353d1a74127a881638978
