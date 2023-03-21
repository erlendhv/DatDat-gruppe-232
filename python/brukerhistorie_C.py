import sqlite3


def brukerhistorie_c():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    stasjon = input("Skriv inn stasjon: ")
    dag = input("Skriv inn ukedag: ")

    cursor.execute('''select Stasjonsnavn, Avgangstid, Ankomsttid, TogruteID, Ukedag from StasjonerITabell natural join 
                   (select * from Togrutetabell natural join 
                    (select * from TogruteForekomst where Ukedag = ?)) where Stasjonsnavn = ?''', (dag, stasjon))
    forekomster = cursor.fetchall()
    print("(Stasjonsnavn, Avgangstid, Ankomsttid, TogruteID, Ukedag))")
    for forekomst in forekomster:
        print(forekomst)

    con.close()
