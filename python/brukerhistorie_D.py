import sqlite3
import datetime
from python.hjelpemetoder import *


def brukerhistorie_d():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    startStasjon = input("Skriv inn ønsket startstasjon: ")
    sluttStasjon = input("Skriv inn ønsket sluttstasjon: ")
    dato_str = input("Angi ønsket dato (YYYY-MM-DD): ")
    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)
    klokkeslett = input("Angi ønsket klokkeslett (hh:mm): ")
    klokkeslett += ":00"

    ukedag1 = dato1.weekday()
    if ukedag1 == 6:
        ukedag2 = 0
    else:
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

    con.close()
