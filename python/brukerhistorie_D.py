import sqlite3
import datetime
from python.hjelpemetoder import *
import re


def brukerhistorie_d():
    '''
    Brukerhistorie D: Som bruker ønsker jeg å søke etter togruter som går mellom 
    to stasjoner med utgangspunkt i dato og klokkeslett. Alle ruter den samme dagen 
    etter gitt klokkeslett og alle ruter neste dag returneres. 
    Først hentes startstasjon, sluttstasjon, dato og klokkeslett fra bruker.
    Deretter hentes alle togruter som går mellom de to stasjonene ved hjelp av metoden findTogruteID.
    Deretter hentes alle avganger fra startstasjonen som er etter klokkeslettet og som er på ukedage1 ved å
    joine TogruteForekomst, TogruteTabell og StasjonerITabell.
    Deretter hentes alle avganger fra startstasjonen som er på ukedag2 ved å joine
    TogruteForekomst, TogruteTabell og StasjonerITabell.
    Til slutt printes resultatet.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    startStasjon = validJernbanestasjon(
        input("Skriv inn ønsket startstasjon: "))

    sluttStasjon = validJernbanestasjon(
        input("Skriv inn ønsket sluttstasjon: "))

    dato_str = dateCheck(input("Angi ønsket dato (YYYY-MM-DD): "))

    year, month, day = map(int, dato_str.split("-"))
    dato1 = datetime.date(year, month, day)

    time_regex = r'^\d{2}:\d{2}$'
    klokkeslett = input("Angi ønsket klokkeslett (hh:mm): ")
    match = re.match(time_regex, klokkeslett)
    while not match:
        print("Klokkeslett er på feil format")
        klokkeslett = input("Angi ønsket klokkeslett (hh:mm): ")
        match = re.match(time_regex, klokkeslett)
    klokkeslett += ":00"

    # Gjør om dato til ukedag, hvor mandag = 0, tirsdag = 1, osv. Helt til søndag = 6.
    ukedag1 = dato1.weekday()

    # Hvis søndag er valgt dag, skal mandag være neste dag, altså lik 0.
    if ukedag1 == 6:
        ukedag2 = 0
    else:
        ukedag2 = ukedag1 + 1  # ellers blir neste dag lik ukedag + 1

    # hjelpemetoder, finnes i klassen hjelpemetoder.py
    ukedag1 = toWeekday(ukedag1)

    ukedag2 = toWeekday(ukedag2)

    godkjentTogID = findTogruteID(startStasjon, sluttStasjon)
    if len(godkjentTogID) == 0:
        print("Fant ingen togruter mellom de to stasjonene.")
        return

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
