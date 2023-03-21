import sqlite3
import datetime


def brukerhistorie_h():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

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

    con.close()
