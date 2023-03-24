import sqlite3
from python.hjelpemetoder import *


def brukerhistorie_c():
    ''''
    Brukerhistorie C: Se info om togrute innom en stasjon. 
    Dette gjøres ved å skrive inn stasjon og ukedag, 
    og så joine Togruteforekomst, TogruteTabell for å finne for å kunne velge passende stasjon og ukedag.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    stasjon = validJernbanestasjon(input("Skriv inn stasjon: "))

    dag = input("Skriv inn ukedag: ").lower()

    # tar natural join på StasjonerITabell, TogruteTabell og Togruteforekomst hvor ukedag i TogruteForekomst
    # er oppgitt ukedag og Stasjonsnavn i StasjonerITabell er oppgitt stasjon.
    cursor.execute('''select Stasjonsnavn, Avgangstid, Ankomsttid, TogruteID, Ukedag from StasjonerITabell natural join 
                   (select * from Togrutetabell natural join 
                    (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?''', (dag, stasjon))
    forekomster = cursor.fetchall()
    if len(forekomster) == 0:
        con.close()
        return print("Fant ingen forekomster for stasjonen " + stasjon + " på ukedag " + dag)
    print("(Stasjonsnavn, Avgangstid, Ankomsttid, TogruteID, Ukedag)")
    for forekomst in forekomster:
        print(forekomst)

    con.close()
