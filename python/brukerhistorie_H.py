import sqlite3
import datetime


def brukerhistorie_h():
    '''
    Brukerhistorie H: Se info om bestillinger
    Dette gjøres ved å skrive inn telefonnummer og epost,
    og så joine Kundeordre, Kunde for å finne passende kunde.
    Deretter henter vi ut alle billetter som er knyttet til funnet kunde, og som er etter dagens dato. 

    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    tlf = input("Oppgi telefonnummer: ")
    while tlf.isdigit() == False:
        print("Telefonnummer må bestå av tall")
        tlf = input("Oppgi telefonnummer: ")
    currentDato = datetime.date.today()

    # Henter ut kundeordre for kunden som har oppgitt telefonnummer og epost
    cursor.execute(
        "SELECT * FROM Kundeordre NATURAL JOIN Kunde WHERE Mobilnummer = ?", (tlf, ))
    resultat = cursor.fetchall()
    if len(resultat) == 0:
        con.close()
        return print("Fant ingen bestillinger for kunden med tlf: " + tlf)
    print("Alle kundeordrer for denne kunden: ")
    for i in resultat:
        print(i)

    # Henter ut billetter fra SeteBillett og SoveBillett som er knyttet til kundens ordrenummer
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
    print("Kommende billetter for denne kunden: ")
    print("(BillettNr, BillettDato, Startstasjon, Endestasjon, KupeeNr/SeteNr, VognID, Ordrenummer)")
    # Printer ut billetter som er etter dagens dato
    for i in billetter:
        if datetime.datetime.strptime(i[1], '%Y-%m-%d').date() >= currentDato:
            print(i)

    con.close()
