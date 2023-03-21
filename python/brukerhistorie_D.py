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

    # Gjør om dato til ukedag, hvor mandag = 0, tirsdag = 1, osv. Helt til søndag = 6.
    ukedag1 = dato1.weekday()

    # Hvis søndag er valgt dag, skal mandag være neste dag, altså lik 0.
    if ukedag1 == 6:
        ukedag2 = 0
    else:
        ukedag2 = ukedag1 + 1  # ellers blir neste dag lik ukedag + 1

    # hjelpemetoder, finnees i klassen hjelpemetoder.py
    ukedag1 = toWeekday(ukedag1)

    ukedag2 = toWeekday(ukedag2)

    godkjentTogID = findTogruteID(startStasjon, sluttStasjon)

    avgangsListe = []
    # Henter alle avganger fra startstasjonen som er etter klokkeslettet og som er på ukedage1.
    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join
        (select * from TogruteTabell natural join
        (select * from TogruteForekomst where Ukedag = ?))
        where Avgangstid >= ? and Stasjonsnavn = ? order by Avgangstid''', (ukedag1, klokkeslett, startStasjon))
    avgangs = cursor.fetchall()
    for i in avgangs:
        avgangsListe.append(i)

    # Henter alle avganger fra startstasjonen som er på ukedag2.
    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join
        (select * from TogruteTabell natural join
        (select * from TogruteForekomst where Ukedag = ?))
        where Stasjonsnavn = ? order by Avgangstid''', (ukedag2, startStasjon))
    avgangs = cursor.fetchall()
    for i in avgangs:
        avgangsListe.append(i)

    # Hvis TogruteID er en togrute som finnes mellom de to stasjonene, printes den.
    print("('Startstasjon', 'Avgangstid', 'TogruteID', 'Ukedag')")
    for i in avgangsListe:
        if i[2] in godkjentTogID:
            print(i)

    con.close()
