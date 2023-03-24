import sqlite3
import datetime
from python.hjelpemetoder import *


def brukerhistorie_g():
    '''
    Dette er brukerhistorie G: Kjøp billett
    Dette gjøres ved å hente telefonnummer, startstasjon, sluttstasjon og dato fra bruker.
    Deretter sjekkes det om kunden finnes i databasen, og om det finnes en rute mellom start og sluttstasjon, 
    og alle togruter som passer med delstrekningene.
    Videre henter vi Sitte eller Sove bilett fra bruker.
    Avhengig av om bruker velger Sitte eller Sove:
        Sjekkes det om det er ledige seter på valgt togrute og får så brukeren til å velge sete.
        Sjekkes om det er ledige kupeer på valgt togrute og får så brukeren til å velge kupe.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    # Finner informasjon om kunden ved oppgitt telefonnummer
    tlf = input("Oppgi telefonnummer: ")
    while tlf.isdigit() == False:
        print("Telefonnummer må bestå av tall")
        tlf = input("Oppgi telefonnummer: ")

    cursor.execute(
        "SELECT * FROM Kunde WHERE Mobilnummer = ?", (tlf,))

    # Sjekker om kunden finnes i databasen
    kundeResultat = cursor.fetchall()
    if len(kundeResultat) == 0:
        print("Det finnes ingen kunder registrert med dette telefonnummeret")
        con.close()
        return

    startStasjon = validJernbanestasjon(
        input("Skriv inn ønsket startstasjon: "))
    sluttStasjon = validJernbanestasjon(
        input("Skriv inn ønsket sluttstasjon: "))

    # Finner ukedag til dato
    dato_str = dateCheck(input("Angi ønsket dato (YYYY-MM-DD): "))

    if startStasjon == "" or sluttStasjon == "" or dato_str == "":
        print("Du må fylle ut alle feltene")
        con.close()
        return
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    ukedag1 = dato1.weekday()

    ukedag1 = toWeekday(ukedag1)

    # Finner alle delstrekninger mellom start og sluttstasjon
    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    if len(delstrekninger) == 0:
        print("Det finnes ingen rute mellom disse stasjonene")
        con.close()
        return
    # En liste med Id til alle delstrekninger til valgt rute
    delstrekningID = []
    for i in delstrekninger:
        delstrekningID.append(i[0])

    # Finner alle togruter som passer med delstrekningene
    togruteID = findTogruteID(startStasjon, sluttStasjon)
    if len(togruteID) == 0:
        print("Det finnes ingen rute mellom disse stasjonene")
        con.close()
        return
    print("Skriv inn ønsket TogruteID fra listen under på formen")
    print("(Startstasjon, TogruteID, AvgangsTid)")
    for i in togruteID:
        cursor.execute(
            '''select * from TogruteForekomst where TogruteID = ? and Ukedag = ?''', (i, ukedag1))
        valid = cursor.fetchall()
        if len(valid) != 0:
            cursor.execute(
                '''select Stasjonsnavn, TogruteTabellID, Avgangstid from stasjoneritabell where 
                (togrutetabellid = ?) and stasjonsnavn = ?''', (i, startStasjon))
            print(cursor.fetchall())

    valgtTogruteID = input("Skriv inn ønsket TogruteID: ")
    # Denne løkken passer på at brukeren skriver inn en gyldig TogruteID
    while valgtTogruteID == "" or not valgtTogruteID.isnumeric():
        valgtTogruteID = input("Skriv inn ønsket TogruteID: ")
    cursor.execute(
        '''select Strekningsnavn from Togrute where TogruteID = ?''', (valgtTogruteID,))
    strekningsnavn = cursor.fetchall()[0][0]

    typeBillett = input("Skriv inn type billett (Sitte/Sove): ")
    while typeBillett == "":
        typeBillett = input("Skriv inn type billett (Sitte/Sove): ")

    # Sjekker om det er ledige sitte-seter på valgt togrute
    if typeBillett == "Sitte":
        opptatteSeter = []

        # Finner alle seter som er opptatt på valgt togrute
        for i in delstrekningID:
            cursor.execute(
                '''select StrekningsID, SeteNr, SittevognID from SeteBillettTilhørerDelstrekning 
                where StrekningsID = ? and BillettDato = ?''', (i, dato1))
            resultat = cursor.fetchall()
            for x in resultat:
                opptatteSeter.append(x)
        cursor.execute('''select * from Sete''')
        seter = cursor.fetchall()

        cursor.execute(
            '''select SittevognID from BestårAv where TogruteID = ?''', (valgtTogruteID,))
        vogner = cursor.fetchall()
        # Liste over ID til alle vogner på valgt togrute
        vognIDList = []
        for i in vogner:
            vognIDList.append(i[0])
        if len(vognIDList) == 0:
            print("Det er ingen passende vogner på valgt togrute")
            return
        ledigeSeterList = []
        # Finner alle ledige seter på valgt togrute
        for i in seter:
            if i[1] in vognIDList:
                ledigeSeterList.append(i)
        fjernPlasser = []
        # Finner alle opptatte seter på valgt togrute
        for i in ledigeSeterList:
            for x in opptatteSeter:
                if i[0] == x[1] and i[1] == x[2]:
                    fjernPlasser.append(i)
        fjernPlasser = set(fjernPlasser)
        # Fjerner alle opptatte seter fra listen over ledige seter
        for i in fjernPlasser:
            ledigeSeterList.remove(i)
        print("Ledige seter på formen: ")
        print("(SeteNr, SittevognID)")
        for i in ledigeSeterList:
            print(i)

        # Sjekker om det er nok ledige seter på valgt togrute
        antallBilletter = int(input("Skriv inn antall billetter: "))
        if antallBilletter > len(ledigeSeterList):
            print("Det er ikke nok ledige seter på dette toget")
            con.close()
            return
        seteNrList = []
        sittevognIDList = []
        kjøpt = []

        # Spør bruker om ønsket seter
        for i in range(antallBilletter):
            seteNr = int(input("Skriv inn ønsket seteNr: "))
            sittevognID = int(input("Skriv inn ønsket sittevognID: "))

            # Sjekker om bruker oppgir gyldige seter
            while (seteNr, sittevognID) in kjøpt:
                print("Setet er allerede valgt")
                seteNr = int(input("Skriv inn ønsket seteNr: "))
                sittevognID = int(input("Skriv inn ønsket sittevognID: "))

            while (seteNr, sittevognID) not in ledigeSeterList:
                print("Setet er ikke ledig/eksisterer ikke")
                seteNr = int(input("Skriv inn ønsket seteNr: "))
                sittevognID = int(input("Skriv inn ønsket sittevognID: "))

            seteNrList.append(seteNr)
            sittevognIDList.append(sittevognID)
            kjøpt.append((seteNr, sittevognID))

        # Kjøper billett hvis gyldige seter er oppgitt
        buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett,
                  tlf, sittevognIDList, seteNrList, antallBilletter, strekningsnavn)

    # Tilsvarende som for sitte-seter, bare for sovekupéer
    elif typeBillett == "Sove":
        # Finner alle kupeer som er opptatt på valgt togrute
        opptatteKupeer = []
        cursor.execute(
            '''select Strekningsnavn from Delstrekning where StrekningsID = ?''', (delstrekningID[0],))
        resultat = cursor.fetchone()
        cursor.execute(
            '''select Strekningsnavn, KupeeNr, SovevognID from SoveBillettTilhørerBanestrekning 
                where StrekningsNavn = ? and BillettDato = ?''', (resultat[0], dato1))
        resultat = cursor.fetchall()
        for x in resultat:
            opptatteKupeer.append(x)
        # Henter alle kupeer
        cursor.execute('''select * from Kupee''')
        kupeer = cursor.fetchall()
        # Henter alle vogner på valgt togrute
        cursor.execute(
            '''select SovevognID from BestårAv where TogruteID = ?''', (valgtTogruteID,))
        vogner = cursor.fetchall()
        # Liste over ID til alle vogner på valgt togrute
        vognIDList = []
        for i in vogner:
            vognIDList.append(i[0])
        vogner = []
        for i in vognIDList:
            if i != None:
                vogner.append(i)

        if len(vogner) == 0:
            print("Det er ingen passende vogner på valgt togrute")
            return
        kupeeIDList = []
        # Finner alle ledige kupeer på valgt togrute
        for i in kupeer:
            if i[1] in vognIDList:
                kupeeIDList.append(i)
        # Lager liste over alle opptatte kupeer på valgt togrute
        fjernPlasser = []
        for i in kupeeIDList:
            for x in opptatteKupeer:
                if i[0] == x[1] and i[1] == x[2]:
                    fjernPlasser.append(i)
        fjernPlasser = set(fjernPlasser)
        # Fjerner alle opptatte kupeer fra listen over ledige kupeer
        for i in fjernPlasser:
            kupeeIDList.remove(i)

        print("Ledige kupeer på formen: ")
        print("(KupeeNr, SovevognID)")
        for i in kupeeIDList:
            print(i)
        # Sjekker om det er nok ledige kupeer på valgt togrute
        antallBilletter = int(input("Skriv inn antall billetter: "))
        if antallBilletter > len(kupeeIDList):
            print("Det er ikke nok ledige kupeer på dette toget")
            con.close()
            return
        kupeeNrList = []
        sovevognIDList = []
        kjøpt = []

        # Spør bruker om ønsket kupeer
        for i in range(antallBilletter):
            kupeeNr = int(input("Skriv inn ønsket kupeeNr: "))
            sovevognID = int(input("Skriv inn ønsket sovevognID: "))

            # Sjekker om bruker oppgir gyldige kupeer
            while (kupeeNr, sovevognID) in kjøpt:
                print("Kupee er allerede valgt")
                kupeeNr = int(input("Skriv inn ønsket kupeeNr: "))
                sovevognID = int(input("Skriv inn ønsket sovevognID: "))

            while (kupeeNr, sovevognID) not in kupeeIDList:
                print("Kupee er ikke ledig/eksisterer ikke")
                con.close()
                return

            kupeeNrList.append(kupeeNr)
            sovevognIDList.append(sovevognID)
            kjøpt.append((kupeeNr, sovevognID))

        # Kjøper billett hvis gyldige kupeer er oppgitt
        buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett,
                  tlf, sovevognIDList, kupeeNrList, antallBilletter, strekningsnavn)

    else:
        print("Ugyldig type billett")

    con.close()

# Funksjon som kjøper valgt billett


def buyTicket(startStasjon, sluttStasjon, dato1, ukedag1, typeBillett, tlf, vognID, seteKupeeNr, antallBilletter, strekningsnavn):
    '''
    Denne funksjonen legger inn all informasjon som vi har funnet i funksjonen brukerhistorie_g, og legger det inn i databasen i tabellene
    avhengig av om man har valgt sittebilett eller sovebilett.
        Ved Sittebillett legges informasjonen inn i tabellene SeteBilettTilhørerBanestrekning, Sittebilett og kundeordre.
        Ved Sovebillett legges informasjonen inn i tabellene SoveBilettTilhørerBanestrekning, Sovebilett og kundeordre.
    '''
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

    delstrekningID = []
    for i in delstrekninger:
        delstrekningID.append(i[0])

    cursor.execute(
        "SELECT Kundenummer FROM KUNDE WHERE Mobilnummer = ?", (tlf,))
    kundenummer = cursor.fetchone()
    if len(kundenummer) != 0:
        kundenummer = kundenummer[0]

    ordrenummer = 0
    cursor.execute(
        "select Ordrenummer from Kundeordre order by Ordrenummer asc")
    ordrenummer1 = cursor.fetchall()

    # Finner ordrenummeret til den nye ordren
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
        # Finner setebillettID til den nye setebilletten som er 1 større enn den siste setebilletten
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

        # Legger inn informasjonen i tabellene SeteBillettTilhørerBanestrekning, SeteBillett og Kundeordre
        # Hvis det er unique constraint feil, så vil en feilmelding bli printet ut
        try:
            for x in range(int(antallBilletkjøp)):
                for i in delstrekningID:
                    cursor.execute(
                        "insert into SeteBillettTilhørerDelstrekning values (?, ?, ?, ?, ?, ?, ?)", (i, billettDato, seteNr[x], sittevognID[x], strekningsnavn, setebillettID, ordrenummer))
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
        # Finner sovebillettID til den nye sovebillett som er 1 større enn den siste sovebillettIDen
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

        # Legger inn informasjonen i tabellene SoveBillettTilhørerBanestrekning, SoveBillett og Kundeordre
        # Hvis det er unique constraint feil, så vil en feilmelding bli printet ut
        try:
            for x in range(antallBilletkjøp):
                cursor.execute(
                    "insert into SoveBillettTilhørerBanestrekning values (?, ?, ?, ?, ?, ?)", (billettDato, KupeeNr[x], SovevognID[x], strekningsnavn, sovebillettID, ordrenummer))
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
