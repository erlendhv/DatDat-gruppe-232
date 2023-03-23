import sqlite3
import datetime


def brukerhistorie_h():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    tlf = input("Oppgi telefonnummer: ")
    currentDato = datetime.date.today()

    # Henter ut kundeordre for kunden som har oppgitt telefonnummer og epost
    cursor.execute(
        "SELECT * FROM Kundeordre NATURAL JOIN Kunde WHERE Mobilnummer = ?", (tlf, ))
    resultat = cursor.fetchall()
    if len(resultat) == 0:
        con.close()
        return print("Fant ingen kundeordre for kunden med tlf: " + tlf)
    print("Kundeordrer for denne kunden: ")
    for i in resultat:
        print(i)

    # Henter ut billetter fra kundeorde som kunde har gjort som er i fremtiden
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
    for i in billetter:
        if datetime.datetime.strptime(i[1], '%Y-%m-%d').date() >= currentDato:
            print(i)

    con.close()
