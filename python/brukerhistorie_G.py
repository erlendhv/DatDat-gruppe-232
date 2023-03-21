import sqlite3
import datetime
from python.hjelpemetoder import *


def brukerhistorie_g():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    # Finner informasjon om kunden ved oppgitt telefonnummer
    tlf = input("Oppgi telefonnummer: ")

    cursor.execute(
        "SELECT * FROM Kunde WHERE Mobilnummer = ?", (tlf,))

    # Sjekker om kunden finnes i databasen
    kundeResultat = cursor.fetchall()
    if len(kundeResultat) == 0:
        print("Det finnes ingen kunder registrert med dette telefonnummeret")
        con.close()
        return
    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")

    # Finner ukedag til dato
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    ukedag1 = dato1.weekday()

    ukedag1 = toWeekday(ukedag1)

    # Finner alle delstrekninger mellom start og sluttstasjon
    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])

    # Finner alle togruter som passer med delstrekningene
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

    # Sjekker om det er ledige sitte-seter på valgt togrute
    if typeBillett == "Sitte":
        opptatteSeter = []

        # Finner alle seter som er opptatt på valgt togrute
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

        # Sjekker om det er nok ledige seter på valgt togrute
        antallBilletter = int(input("Skriv inn antall billetter: "))
        if antallBilletter > len(seterFint):
            print("Det er ikke nok ledige seter på dette toget")
            con.close()
            return
        seteNrList = []
        sittevognIDList = []

        # Sjekker om bruker oppgir gyldige seter
        for i in range(antallBilletter):
            seteNrList.append(int(input("Skriv inn ønsket seteNr: ")))
            sittevognIDList.append(
                int(input("Skriv inn ønsket sittevognID: ")))
            if (seteNrList[i], sittevognIDList[i]) not in seterFint:
                print("Setet er ikke ledig/eksisterer ikke")
                con.close()
                return

        # Kjøper billett hvis gyldige seter er oppgitt
        buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett,
                  tlf, sittevognIDList, seteNrList, antallBilletter)

    # Tilsvarende som for sitte-seter, bare for sovekupéer
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
            con.close()
            return
        kupeeNrList = []
        sovevognIDList = []

        for i in range(antallBilletter):
            kupeeNrList.append(int(input("Skriv inn ønsket kupeeNr: ")))
            sovevognIDList.append(int(input("Skriv inn ønsket sovevognID: ")))
            if (kupeeNrList[i], sovevognIDList[i]) not in kupeerFint:
                print("Kupee er ikke ledig/eksisterer ikke")
                con.close()
                return
        buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett,
                  tlf, sovevognIDList, kupeeNrList, antallBilletter)

    else:
        print("Ugyldig type billett")

    con.close()

# Funksjon som kjøper billett


def buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett, tlf, vognID, seteKupeeNr, antallBilletter):
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    # Finner dagens dato og tid
    billettDato = dato1
    ordreDato = datetime.date.today()
    ordreTid = datetime.datetime.now().time()
    ordreTid = ordreTid.strftime("%H:%M:%S")
    ukedag1 = ukedag1.lower()

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)

    togruteID = findTogruteID(startStasjon, sluttStasjon)

    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])

    cursor.execute(
        "SELECT Kundenummer FROM KUNDE WHERE Mobilnummer = ?", (tlf,))
    kundenummer = cursor.fetchone()
    if len(kundenummer) != 0:
        kundenummer = kundenummer[0]

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

    con.close()
