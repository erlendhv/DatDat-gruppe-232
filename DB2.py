# New file
import sqlite3
import datetime
con = sqlite3.connect('232DB.db')
cursor = con.cursor()


def rukerhistorie_c():
    stasjon = input("Skriv inn stasjon: ")
    dag = input("Skriv inn dag: ")

    cursor.execute("select TogruteID from StasjonerITabell natural join (select * from Togrutetabell natural join (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?", (dag, stasjon))
    forekomster = cursor.fetchall()
    print(forekomster)


def Brukerhistorie_d():
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    klokkeslett = input("Angi ønsket klokkeslett (hh:mm): ")
    klokkeslett += ":00"

    ukedag1 = dato1.today().weekday()
    ukedag2 = ukedag1 + 1
    match ukedag1:
        case 0:
            ukedag1 = "Mandag"
        case 1:
            ukedag1 = "Tirsdag"
        case 2:
            ukedag1 = "Onsdag"
        case 3:
            ukedag1 = "Torsdag"
        case 4:
            ukedag1 = "Fredag"
        case 5:
            ukedag1 = "Lørdag"
        case 6:
            ukedag1 = "Søndag"

    match ukedag2:
        case 0:
            ukedag2 = "Mandag"
        case 1:
            ukedag2 = "Tirsdag"
        case 2:
            ukedag2 = "Onsdag"
        case 3:
            ukedag2 = "Torsdag"
        case 4:
            ukedag2 = "Fredag"
        case 5:
            ukedag2 = "Lørdag"
        case 6:
            ukedag2 = "Søndag"

    cursor.execute('''select Startstasjon, Endestasjon, Avgangstid, TogruteID, Ukedag from StasjonerITabell join
    (select TogruteTabellID as TabellID, TogruteID, Ukedag, Startstasjon, EndeStasjon from TogruteTabell natural join
    (select * from TogruteForekomst natural join (select * from TogruteHarDelstrekning natural join
    (select * from Delstrekning where Startstasjon = ? and EndeStasjon = ?))
    where Ukedag = ? or Ukedag = ?)) on TabellID = TogruteTabellID and Startstasjon = Stasjonsnavn
    where Avgangstid >= ?''', (startStasjon, sluttStasjon, ukedag1, ukedag2, klokkeslett))

    avgangs = cursor.fetchall()
    print(avgangs)

# cursor.execute('''select * from StasjonerITabell natural join
# (select * from TogruteForekomst natural join
# TogruteTabell where Ukedag = ? or Ukedag = ?)
# where Stasjonsnavn = ? and Avgangstid != "" and Avgangstid >= ? ''', (ukedag1, ukedag2, startStasjon, klokkeslett))

# avgangs = cursor.fetchall()

# cursor.execute('''select * from StasjonerITabell natural join
# (select * from TogruteForekomst natural join
# TogruteTabell where Ukedag = ? or Ukedag = ?)
# where Stasjonsnavn = ? and Ankomsttid != ""''', (ukedag1, ukedag2, sluttStasjon))

# ankomster = cursor.fetchall()

# for i in avgangs:
#     for j in ankomster:
#         if i[5] == j[5] and i[4] == j[4]:
#             if i[2] is not None and j[3] is not None:
#                 if i[2] <= j[3]:
#                     print(i + j)


def brukerhistorie_e():
    Kundenummer = 0
    cursor.execute("select Kundenummer from Kunde order by Kundenummer asc")
    Kundenummer1 = cursor.fetchall()
    print(Kundenummer1)

    if len(Kundenummer1) == 0:
        Kundenummer = 0
    elif len(Kundenummer1) == 1:
        Kundenummer = Kundenummer1[0][0]
    else:
        Kundenummer = Kundenummer1[-1][0]
    Kundenummer += 1
    Kundenavn = input("Skriv inn navnet ditt: ")
    Epost = input("Skriv inn E-post: ")
    Mobilnummer = input("Skriv inn mobilnummer: ")

    cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''',
                   (Kundenummer, Kundenavn, Epost, Mobilnummer))

    con.commit()


def brukerhistorie_g():
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    typeBillett = input("Skriv inn type billett (Sitte/Sove): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    ukedag1 = dato1.today().weekday()
    match ukedag1:
        case 0:
            ukedag1 = "Mandag"
        case 1:
            ukedag1 = "Tirsdag"
        case 2:
            ukedag1 = "Onsdag"
        case 3:
            ukedag1 = "Torsdag"
        case 4:
            ukedag1 = "Fredag"
        case 5:
            ukedag1 = "Lørdag"
        case 6:
            ukedag1 = "Søndag"

    tlf = input("Oppgi telefonnummer: ")

    cursor.execute(
        "SELECT * FROM Kunde WHERE Mobilnummer = ?", (tlf,))

    resultat = cursor.fetchall()

    if len(resultat) != 0 and typeBillett == "Sitte":
        cursor.execute(
            '''select * from SeteBillettTilhørerDelstrekning natural join 
            (SELECT * FROM Delstrekning WHERE Startstasjon = ? AND Endestasjon = ?) where 
            BillettDato = ?''', (startStasjon, sluttStasjon, dato1))
        resultat = cursor.fetchall()

    if len(resultat) != 0 and typeBillett == "Sove":
        cursor.execute(
            '''select * from SoveBillettTilhørerDelstrekning natural join 
            (SELECT * FROM Delstrekning WHERE Startstasjon = ? AND Endestasjon = ?) where 
            BillettDato = ?''', (startStasjon, sluttStasjon, dato1))
        resultat = cursor.fetchall()


def buyTicket():
    e_post = input("Skriv inn e-post: ")
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    typeBillett = input("Skriv inn type billett (Sitte/Sove): ")
    year, month, day = map(int, dato_str.split("-"))
    billettDato = datetime.date(year, month, day)
    ordreDato = datetime.date.today()
    ordreTid = datetime.datetime.now().time()
    ordreTid = ordreTid.strftime("%H:%M:%S")
    ukedag1 = billettDato.today().weekday()
    match ukedag1:
        case 0:
            ukedag1 = "Mandag"
        case 1:
            ukedag1 = "Tirsdag"
        case 2:
            ukedag1 = "Onsdag"
        case 3:
            ukedag1 = "Torsdag"
        case 4:
            ukedag1 = "Fredag"
        case 5:
            ukedag1 = "Lørdag"
        case 6:
            ukedag1 = "Søndag"

    cursor.execute(
        "SELECT StrekningsID FROM Delstrekning WHERE Startstasjon = ? AND Endestasjon = ?", (startStasjon, sluttStasjon))
    strekningsID = cursor.fetchall()[0][0]
    cursor.execute(
        "select TogruteID from TogruteForekomst natural join TogruteHarDelstrekning where StrekningsID = ? and Ukedag = ?", (strekningsID, ukedag1))
    togruteID = cursor.fetchall()[0][0]
    cursor.execute(
        "SELECT Kundenummer FROM KUNDE WHERE Epost = ?", (e_post,))
    kundenummer = cursor.fetchall()[0][0]
    ordrenummer = 0
    cursor.execute(
        "select Ordrenummer from Kundeordre order by Ordrenummer asc")
    ordrenummer1 = cursor.fetchall()

    if len(ordrenummer1) == 0:
        ordrenummer = 0
    elif len(ordrenummer1) == 1:
        ordrenummer = ordrenummer1[0][0]
    else:
        ordrenummer = ordrenummer1[-1][0]
    ordrenummer += 1
    cursor.execute(
        "INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?, ?)", (ordrenummer, ordreDato, ordreTid, 1, kundenummer, ukedag1, togruteID))
    con.commit()
    if typeBillett == "Sitte":
        cursor.execute(
            "select * from SeteBillett")
        setebillett = cursor.fetchall()
        setebillettID = 0
        if len(setebillett) == 0:
            setebillettID = 0
        elif len(setebillett) == 1:
            setebillettID = setebillett[0][0]
        else:
            setebillettID = setebillett[-1][0]
        setebillettID += 1

        cursor.execute(
            "insert into SeteBillett values (?, ?, ?, ?, ?, ?, ?)", (setebillettID, billettDato, startStasjon, sluttStasjon, 1, 1, ordrenummer))
        con.commit()

    cursor.execute(
        "SELECT * FROM Kundeordre")
    kundeordre = cursor.fetchall()
    print(kundeordre)
    cursor.execute(
        "SELECT * FROM SeteBillett")
    setebillett = cursor.fetchall()
    print(setebillett)


def brukerhistorie_h():
    tlf = input("Oppgi telefonnummer: ")
    epost = input("Oppgi epostadresse: ")

    cursor.execute(
        "SELECT * FROM Kundeordre NATURAL JOIN Kunde WHERE Mobilnummer = ? AND Epost = ?", (tlf, epost))
    resultat = cursor.fetchall()
    print(resultat)


def printKunder():
    cursor.execute("SELECT * FROM Kunde")
    kunder = cursor.fetchall()
    print(kunder)

# con.close()


if __name__ == "__main__":
    # brukerhistorie_e()
    buyTicket()
    # brukerhistorie_h()
    printKunder()

# Midlertidig
# cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
#     (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
#         tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
#             Ukedag = ?) AND Startstasjon = ? AND Sluttstasjon = ? \
#     AND Avgangstid >= ? ORDER BY Klokkeslett", (ukedag1, ukedag2, startStasjon, sluttStasjon, klokkeslett))
# resultat = cursor.fetchall()
# print(resultat)


# cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
#     (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
#         tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
#             Ukedag = ?) AND Startstasjon = ? AND Sluttstasjon = ? \
#     AND Avgangstid >= ? ORDER BY Klokkeslett", (ukedag1, ukedag2, startStasjon, sluttStasjon, klokkeslett))
# resultat = cursor.fetchall()
# print(resultat)
