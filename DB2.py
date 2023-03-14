# New file
import sqlite3, datetime
con = sqlite3.connect('232DB.db')
cursor = con.cursor()


# Brukerhistorie c
# stasjon = input("Skriv inn stasjon: ")
# dag = input("Skriv inn dag: ")

# cursor.execute("select TogruteID from StasjonerITabell natural join (select * from Togrutetabell natural join (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?", (dag, stasjon))
# forekomster = cursor.fetchall()
# print(forekomster)

# Brukerhistorie d
startStasjon = input("Skriv inn ønsket startstasjon: ")
sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
year, month, day = map(int, dato_str.split("-"))
dato1 = datetime.date(year, month, day)
dato2 = dato1 + datetime.timedelta(days=1)
klokkeslett = input("Angi ønsket klokkeslett: ")

ukedag1 = dato1.strftime("%A")
ukedag2 = dato2.strftime("%A")

cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
    (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
        tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
            Ukedag = ?) AND Stasjonsnavn=? \
    AND Avgangstid >= ?", (ukedag1, ukedag2, startStasjon, klokkeslett))
resultat = cursor.fetchall()
print(resultat)

# Brukerhistorie e
# Kundenummer = 0
# cursor.execute("select Kundenummer from Kunde")
# Kundenummer = cursor.fetchall()[-1][0]
# Kundenummer += 1
# Kundenavn = input("Skriv inn navnet ditt: ")
# Epost = input("Skriv inn E-post: ")
# Mobilnummer = input("Skriv inn mobilnummer: ")

# cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''',
#                (Kundenummer, Kundenavn, Epost, Mobilnummer))


con.commit()

con.close()




# "SELECT TogruteID FROM (TogruteForekomst JOIN (StasjonerITabell AS st JOIN Togrutetabell AS tt \
# ON st.TogruteTabellID = tt.TogruteTabellID) ON  WHERE Ukedag = ? OR Ukedag = ? AND Startstasjon = ? AND Sluttstasjon = ? \
# AND Avgangstid >= ?", (ukedag1), (ukedag2), (startStasjon), (sluttStasjon), (klokkeslett))


#ChatGPT
# cursor.execute("SELECT TogruteForekomst.TogruteID FROM TogruteForekomst \
#          JOIN StasjonerITabell AS st ON TogruteForekomst.FraStasjonsID=st.StasjonsID \
#          JOIN Togrutetabell AS tt ON TogruteForekomst.TogruteID=tt.TogruteID \
#          WHERE st.StasjonNavn=? AND tt.Dato=? OR st.Stasjonsnavn=? and tt.Dato = ?", (startStasjon, ukedag1, startStasjon, ukedag2))

# cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
#     (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
#         tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
#             Ukedag = ?) AND Startstasjon = ? AND Sluttstasjon = ? \
#     AND Avgangstid >= ?", (ukedag1, ukedag2, startStasjon, sluttStasjon, klokkeslett))
# resultat = cursor.fetchall()
# print(resultat)