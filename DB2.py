import sqlite3
import datetime
from collections import deque
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

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])
    cursor.execute(
        "SELECT distinct TogruteID FROM Togrute")
    togruteID = cursor.fetchall()
    IDer = []
    for i in togruteID:
        IDer.append(i[0])
    godkjentTogID = []
    for i in IDer:
        cursor.execute(
            "SELECT StrekningsID FROM TogruteHarDelstrekning where TogruteID = ?", (i,))
        TogruteHarDelstrekning = cursor.fetchall()
        penListe = []
        for x in TogruteHarDelstrekning:
            penListe.append(x[0])
        common_list = set(delstrekningIDFint).intersection(penListe)
        if len(common_list) == len(delstrekningIDFint):
            godkjentTogID.append(i)

    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join 
        (select * from TogruteTabell natural join 
        (select * from TogruteForekomst where Ukedag = ? or Ukedag = ?)) 
        where Avgangstid >= ? and Stasjonsnavn = ?''', (ukedag1, ukedag2, klokkeslett, startStasjon))
    avgangs = cursor.fetchall()

    for i in avgangs:
        if i[2] in godkjentTogID:
            print(i)


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


def findDelstrekning(start_station, end_station):
    # create a set to keep track of visited stations
    visited = set()

    # create a queue to store stations to visit
    queue = deque([(start_station, [])])

    # create a list to store all possible routes
    routes = []

    # perform BFS to find all possible routes
    while queue:
        curr_station, curr_route = queue.popleft()
        visited.add(curr_station)

        # if we've reached the end station, add the current route to the list of routes
        if curr_station == end_station:
            routes.append(curr_route + [curr_station])

        # otherwise, add all unvisited stations connected to the current station to the queue
        else:
            cursor.execute(
                "SELECT EndeStasjon FROM Delstrekning WHERE Startstasjon = ?", (curr_station,))
            for next_station in cursor.fetchall():
                if next_station[0] not in visited:
                    queue.append(
                        (next_station[0], curr_route + [curr_station]))

    returnList = []
    for i in range(1, len(routes[0])):
        cursor.execute(
            "SELECT * FROM Delstrekning WHERE Startstasjon = ? AND EndeStasjon = ?", (routes[0][i - 1], routes[0][i]))
        returnList.append(cursor.fetchall()[0])
    return returnList


if __name__ == "__main__":
    print("Velkommen til Togtider AS")
    Brukerhistorie_d()

con.close()
