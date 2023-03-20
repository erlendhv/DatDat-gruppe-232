import sqlite3
import datetime
from collections import deque
con = sqlite3.connect('232DB.db')
cursor = con.cursor()


def brukerhistorie_c():
    stasjon = input("Skriv inn stasjon: ")
    dag = input("Skriv inn dag: ")

    cursor.execute("select TogruteID from StasjonerITabell natural join (select * from Togrutetabell natural join (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?", (dag, stasjon))
    forekomster = cursor.fetchall()
    print(forekomster)


def brukerhistorie_d():
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    klokkeslett = input("Angi ønsket klokkeslett (hh:mm): ")
    klokkeslett += ":00"

    ukedag1 = dato1.weekday()
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

    godkjentTogID = findTogruteID(startStasjon, sluttStasjon)
    # delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    # delstrekningIDFint = []
    # for i in delstrekninger:
    #     delstrekningIDFint.append(i[0])
    # cursor.execute(
    #     "SELECT distinct TogruteID FROM Togrute")
    # togruteID = cursor.fetchall()
    # IDer = []
    # for i in togruteID:
    #     IDer.append(i[0])
    # godkjentTogID = []
    # for i in IDer:
    #     cursor.execute(
    #         "SELECT StrekningsID FROM TogruteHarDelstrekning where TogruteID = ?", (i,))
    #     TogruteHarDelstrekning = cursor.fetchall()
    #     penListe = []
    #     for x in TogruteHarDelstrekning:
    #         penListe.append(x[0])
    #     common_list = set(delstrekningIDFint).intersection(penListe)
    #     if len(common_list) == len(delstrekningIDFint):
    #         godkjentTogID.append(i)

    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join 
        (select * from TogruteTabell natural join 
        (select * from TogruteForekomst where Ukedag = ? or Ukedag = ?)) 
        where Avgangstid >= ? and Stasjonsnavn = ?''', (ukedag1, ukedag2, klokkeslett, startStasjon))

    avgangs = cursor.fetchall()

    print("('Startstasjon', 'Avgangstid', 'TogruteID', 'Ukedag')")
    for i in avgangs:
        if i[2] in godkjentTogID:
            print(i)


def brukerhistorie_e():
    Kundenummer = 0
    cursor.execute("select Kundenummer from Kunde order by Kundenummer asc")
    Kundenummer1 = cursor.fetchall()

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
    print("Kunde registrert")


def brukerhistorie_g():
    tlf = input("Oppgi telefonnummer: ")

    cursor.execute(
        "SELECT * FROM Kunde WHERE Mobilnummer = ?", (tlf,))

    kundeResultat = cursor.fetchall()
    if len(kundeResultat) == 0:
        print("Det finnes ingen kunder registrert med dette telefonnummeret")
        return
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    ukedag1 = dato1.weekday()
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

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])

    togruteID = findTogruteID(startStasjon, sluttStasjon)
    for i in togruteID:
        cursor.execute(
            '''select * from TogruteForekomst where TogruteID = ? and Ukedag = ?''', (i, ukedag1))
        valid = cursor.fetchall()
        if len(valid) != 0:
            cursor.execute(
                '''select * from stasjoneritabell where 
                (togrutetabellid = ?) and stasjonsnavn = ?''', (i, startStasjon))
            print(cursor.fetchall())

    valgtTogruteID = input("Skriv inn ønsket TogruteID: ")
    typeBillett = input("Skriv inn type billett (Sitte/Sove): ")

    if typeBillett == "Sitte":
        opptatteSeter = []

        for i in delstrekningIDFint:
            cursor.execute(
                '''select StrekningsID, SeteNr, SittevognID from SeteBillettTilhørerDelstrekning 
                where StrekningsID = ? and BillettDato = ?''', (i, dato1))
            resultat = cursor.fetchall()
            for x in resultat:
                opptatteSeter.append(x)
        cursor.execute('''select * from Sete''')
        seter = cursor.fetchall()
        seterFint = []
        cursor.execute(
            '''select SittevognID from BestårAv where TogruteID = ?''', (valgtTogruteID,))
        vogner = cursor.fetchall()
        vognFint = []
        for i in vogner:
            vognFint.append(i[0])
        if len(vognFint) == 0:
            print("Det er ingen passende vogner på valgt togrute")
            return
        for i in seter:
            if i[1] in vognFint:
                seterFint.append(i)
        fjern = []
        for i in seterFint:
            for x in opptatteSeter:
                if i[0] == x[1] and i[1] == x[2]:
                    fjern.append(i)
        fjern = set(fjern)
        for i in fjern:
            seterFint.remove(i)
        print("Ledige seter på formen: ")
        print("(SeteNr, SittevognID)")
        print(seterFint)
        # Number of tickets to buy
        antallBilletter = int(input("Skriv inn antall billetter: "))
        if antallBilletter > len(seterFint):
            print("Det er ikke nok ledige seter på dette toget")
            return
        seteNrList = []
        sittevognIDList = []
        # if antallBilletter == 1:
        #     seteNr = input("Skriv inn ønsket seteNr: ")
        #     sittevognID = input("Skriv inn ønsket sittevognID: ")
        #     buyTicket(startStasjon, sluttStasjon, dato_str,
        #               typeBillett, tlf, sittevognID, seteNr, antallBilletter)
        # else:
        for i in range(antallBilletter):
            seteNrList.append(input("Skriv inn ønsket seteNr: "))
            sittevognIDList.append(input("Skriv inn ønsket sittevognID: "))
        buyTicket(startStasjon, sluttStasjon, dato_str,
                  typeBillett, tlf, sittevognIDList, seteNrList, antallBilletter)

    elif typeBillett == "Sove":
        opptatteKupeer = []
        cursor.execute(
            '''select Strekningsnavn from Delstrekning where StrekningsID = ?''', (delstrekningIDFint[0],))
        resultat = cursor.fetchone()
        cursor.execute(
            '''select Strekningsnavn, KupeeNr, SovevognID from SoveBillettTilhørerBanestrekning 
                where StrekningsNavn = ? and BillettDato = ?''', (resultat[0], dato1))
        resultat = cursor.fetchall()
        for x in resultat:
            opptatteKupeer.append(x)
        cursor.execute('''select * from Kupee''')
        kupeer = cursor.fetchall()
        kupeerFint = []
        cursor.execute(
            '''select SovevognID from BestårAv where TogruteID = ?''', (valgtTogruteID,))
        vogner = cursor.fetchall()
        vognFint = []
        for i in vogner:
            vognFint.append(i[0])
        vogner = []
        for i in vognFint:
            if i != None:
                vogner.append(i)

        if len(vogner) == 0:
            print("Det er ingen passende vogner på valgt togrute")
            return
        for i in kupeer:
            if i[1] in vognFint:
                kupeerFint.append(i)
        fjern = []
        for i in kupeerFint:
            for x in opptatteKupeer:
                if i[0] == x[1] and i[1] == x[2]:
                    fjern.append(i)
        fjern = set(fjern)
        for i in fjern:
            kupeerFint.remove(i)

        print("Ledige kupeer på formen: ")
        print("(KupeeNr, SovevognID)")
        print(kupeerFint)
        antallBilletter = int(input("Skriv inn antall billetter: "))
        if antallBilletter > len(kupeerFint):
            print("Det er ikke nok ledige kupeer på dette toget")
            return
        kupeeNrList = []
        sovevognIDList = []
        # if antallBilletter == 1:
        #     kupeeNr = input("Skriv inn ønsket kupeeNr: ")
        #     sovevognID = input("Skriv inn ønsket sovevognID: ")
        #     buyTicket(startStasjon, sluttStasjon, dato_str,
        #               typeBillett, tlf, sovevognID, kupeeNr, antallBilletter)
        # else:
        for i in range(antallBilletter):
            kupeeNrList.append(input("Skriv inn ønsket kupeeNr: "))
            sovevognIDList.append(input("Skriv inn ønsket sovevognID: "))
        buyTicket(startStasjon, sluttStasjon, dato_str,
                  typeBillett, tlf, sovevognIDList, kupeeNrList, antallBilletter)

        # kupeeNr = input("Skriv inn ønsket kupeeNr: ")
        # sovevognID = input("Skriv inn ønsket sovevognID: ")
        # buyTicket(startStasjon, sluttStasjon, dato_str,
        #   typeBillett, tlf, sovevognID, kupeeNr, antallBilletter)
    else:
        print("Ugyldig type billett")


def brukerhistorie_h():
    tlf = input("Oppgi telefonnummer: ")
    epost = input("Oppgi epostadresse: ")
    currentDato = datetime.date.today()

    cursor.execute(
        "SELECT * FROM Kundeordre NATURAL JOIN Kunde WHERE Mobilnummer = ? AND Epost = ?", (tlf, epost))
    resultat = cursor.fetchall()
    ordreNummer = []
    for ordre in resultat:
        ordreNummer.append(ordre[0])
    billetter = []
    for i in ordreNummer:
        cursor.execute(
            "SELECT * FROM SeteBillett WHERE Ordrenummer = ?", (i,))
        resultat = cursor.fetchall()
        for x in resultat:
            billetter.append(x)
        cursor.execute(
            "SELECT * FROM SoveBillett WHERE Ordrenummer = ?", (i,))
        resultat = cursor.fetchall()
        for z in resultat:
            billetter.append(z)
    for i in billetter:
        # print(i)
        if datetime.datetime.strptime(i[1], '%Y-%m-%d').date() >= currentDato:
            print(i)

    print(resultat)


def printKunder():
    cursor.execute("SELECT * FROM Kunde")
    kunder = cursor.fetchall()
    print(kunder)


def buyTicket(startStasjon, sluttStasjon, dato_str, typeBillett, tlf, vognID, seteKupeeNr, antallBilletter):
    # e_post = input("Skriv inn e-post: ")
    # startStasjon = input("Skriv inn ønsket startstasjon: ")
    # sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    # dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    # typeBillett = input("Skriv inn type billett (Sitte/Sove): ")
    year, month, day = map(int, dato_str.split("-"))
    billettDato = datetime.date(year, month, day)
    ordreDato = datetime.date.today()
    ordreTid = datetime.datetime.now().time()
    ordreTid = ordreTid.strftime("%H:%M:%S")
    ukedag1 = billettDato.weekday()
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

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    # print("Delstrekninger")
    # print(delstrekninger)
    togruteID = findTogruteID(startStasjon, sluttStasjon)
    # print("TogruteID")
    # print(togruteID)
    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])

    # for i in delstrekningIDFint:
    # cursor.execute(
    # "select TogruteID from TogruteForekomst natural join TogruteHarDelstrekning where StrekningsID = ? and Ukedag = ?", (i, ukedag1))
    # togruteID = cursor.fetchall()[0][0]
    # togruteForekomst = []
    # for i in togruteID:
    #     cursor.execute(
    #         "select * from TogruteForekomst where TogruteID = ? and Ukedag = ?", (i, ukedag1))
        # print("togruteForekomst")
        # print(cursor.fetchall())
    # print("TogruteForekomst")
    # print(togruteForekomst)

    cursor.execute(
        "SELECT Kundenummer FROM KUNDE WHERE Mobilnummer = ?", (tlf,))
    kundenummer = cursor.fetchone()
    if len(kundenummer) != 0:
        kundenummer = kundenummer[0]
    # print("Kundenummer")
    # print(kundenummer)
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
    if typeBillett == "Sitte":
        cursor.execute(
            "select * from SeteBillett order by BillettNr asc")
        setebillett = cursor.fetchall()
        setebillettID = 0
        if len(setebillett) == 0:
            setebillettID = 0
        elif len(setebillett) == 1:
            setebillettID = setebillett[0][0]
        else:
            setebillettID = setebillett[-1][0]
        setebillettID += 1

        seteNr = seteKupeeNr
        sittevognID = vognID
        antallBilletkjøp = antallBilletter

        try:
            # if antallBilletkjøp == 1:
            #     for i in delstrekningIDFint:
            #         cursor.execute(
            #             "insert into SeteBillettTilhørerDelstrekning values (?, ?, ?, ?, ?, ?, ?)", (i, billettDato, seteNr, sittevognID, "Nordlandsbanen", setebillettID, ordrenummer))
            #         con.commit()
            #     cursor.execute(
            #         "insert into SeteBillett values (?, ?, ?, ?, ?, ?, ?)", (setebillettID, billettDato, startStasjon, sluttStasjon, seteNr, sittevognID, ordrenummer))
            #     con.commit()
            #     cursor.execute(
            #         "INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?, ?)", (ordrenummer, ordreDato, ordreTid, antallBilletkjøp, kundenummer, ukedag1, togruteID[0]))
            #     con.commit()
            # else:
            for x in range(int(antallBilletkjøp)):
                for i in delstrekningIDFint:
                    cursor.execute(
                        "insert into SeteBillettTilhørerDelstrekning values (?, ?, ?, ?, ?, ?, ?)", (i, billettDato, seteNr[x], sittevognID[x], "Nordlandsbanen", setebillettID, ordrenummer))
                    con.commit()
                cursor.execute(
                    "insert into SeteBillett values (?, ?, ?, ?, ?, ?, ?)", (setebillettID, billettDato, startStasjon, sluttStasjon, seteNr[x], sittevognID[x], ordrenummer))
                con.commit()
                setebillettID += 1
            cursor.execute(
                "INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?, ?)", (ordrenummer, ordreDato, ordreTid, antallBilletkjøp, kundenummer, ukedag1, togruteID[0]))
            con.commit()
            print("Billett(er) kjøpt")
        except sqlite3.Error as error:
            print("Kunne ikke kjøpe billett")
            print(error)
            # cursor.execute(
            #     "delete from Kundeordre where Ordrenummer = ?", (ordrenummer,))
            # con.commit()
    elif typeBillett == "Sove":
        cursor.execute(
            "select * from SoveBillett order by BillettNr asc")
        sovebillett = cursor.fetchall()
        sovebillettID = 0
        if len(sovebillett) == 0:
            sovebillettID = 0
        elif len(sovebillett) == 1:
            sovebillettID = sovebillett[0][0]
        else:
            sovebillettID = sovebillett[-1][0]
        sovebillettID += 1

        KupeeNr = seteKupeeNr
        SovevognID = vognID
        antallBilletkjøp = antallBilletter

        try:
            # for i in delstrekningIDFint:
            # if antallBilletkjøp == 1:
            #     cursor.execute(
            #         "insert into SoveBillettTilhørerBanestrekning values (?, ?, ?, ?, ?, ?)", (billettDato, KupeeNr, SovevognID, "Nordlandsbanen", sovebillettID, ordrenummer))
            #     con.commit()
            #     cursor.execute(
            #         "insert into SoveBillett values (?, ?, ?, ?, ?, ?, ?)", (sovebillettID, billettDato, startStasjon, sluttStasjon, KupeeNr, SovevognID, ordrenummer))
            #     con.commit()
            #     cursor.execute(
            #         "INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?, ?)", (ordrenummer, ordreDato, ordreTid, antallBilletkjøp, kundenummer, ukedag1, togruteID[0]))
            #     con.commit()
            # else:
            for x in range(antallBilletkjøp):
                cursor.execute(
                    "insert into SoveBillettTilhørerBanestrekning values (?, ?, ?, ?, ?, ?)", (billettDato, KupeeNr[x], SovevognID[x], "Nordlandsbanen", sovebillettID, ordrenummer))
                con.commit()
                cursor.execute(
                    "insert into SoveBillett values (?, ?, ?, ?, ?, ?, ?)", (sovebillettID, billettDato, startStasjon, sluttStasjon, KupeeNr[x], SovevognID[x], ordrenummer))
                con.commit()
                sovebillettID += 1
            cursor.execute(
                "INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?, ?)", (ordrenummer, ordreDato, ordreTid, antallBilletkjøp, kundenummer, ukedag1, togruteID[0]))
            con.commit()
            print("Billett(er) kjøpt")

        except sqlite3.Error as error:
            print("Kunne ikke kjøpe billett")
            print(error)
            # cursor.execute(
            #     "delete from Kundeordre where Ordrenummer = ?", (ordrenummer,))
            # con.commit()


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
    try:
        for i in range(1, len(routes[0])):
            cursor.execute(
                "SELECT * FROM Delstrekning WHERE Startstasjon = ? AND EndeStasjon = ?", (routes[0][i - 1], routes[0][i]))
            returnList.append(cursor.fetchall()[0])
    except:
        print("Det finnes ingen delstrekninger mellom disse stasjonene")

    return returnList


def findTogruteID(startStasjon, sluttStasjon):
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
    return godkjentTogID


if __name__ == "__main__":
    print("Velkommen til Togtider AS")
    # brukerhistorie_d()
    # brukerhistorie_h()
    brukerhistorie_g()
    # buyTicket()
    # brukerhistorie_e()
    # printKunder()
    cursor.execute(
        "SELECT * FROM Kundeordre")
    kundeordre = cursor.fetchall()
    print("Kundeordre")
    print(kundeordre)
    cursor.execute(
        "SELECT * FROM SeteBillett")
    setebillett = cursor.fetchall()
    print("Setebillett")
    print(setebillett)
    cursor.execute(
        "SELECT * FROM SoveBillett")
    sovebillett = cursor.fetchall()
    print("Sovebillett")
    print(sovebillett)
    cursor.execute(
        "SELECT * FROM SetebillettTilhørerDelstrekning")
    setebillettTilhørerDelstrekning = cursor.fetchall()
    print("SetebillettTilhørerDelstrekning")
    print(setebillettTilhørerDelstrekning)
    cursor.execute(
        "SELECT * FROM SovebillettTilhørerBanestrekning")
    sovebillettTilhørerBanestrekning = cursor.fetchall()
    print("SovebillettTilhørerBanestrekning")
    print(sovebillettTilhørerBanestrekning)

con.close()
