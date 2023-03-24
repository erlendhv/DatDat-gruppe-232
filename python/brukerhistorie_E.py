import sqlite3


def brukerhistorie_e():
    '''
    Brukerhistorie E: Registrering av ny bruker
    Dette gjøres ved å hente navn, epost og mobilnummer fra brukeren. 
    Denne informasjonen blir så lagt inn i Kundetabellen i databasen.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    Kundenummer = 0
    cursor.execute("select Kundenummer from Kunde order by Kundenummer asc")
    Kundenummer1 = cursor.fetchall()

    # Henter kundenumemret til den siste kunden i databasen og legger til 1 for å gi
    # dette kundenummeret til den nye kunden
    if len(Kundenummer1) == 0:
        Kundenummer = 0
    elif len(Kundenummer1) == 1:
        Kundenummer = Kundenummer1[0][0]
    else:
        Kundenummer = Kundenummer1[-1][0]
    Kundenummer += 1
    Kundenavn = input("Skriv inn navnet ditt: ")
    Epost = input("Skriv inn E-post: ")

    Mobilnummer = input("Skriv inn mobilnummer: ")
    while Mobilnummer.isdigit() == False:
        print("Mobilnummer må bestå av tall")
        Mobilnummer = input("Skriv inn mobilnummer: ")

    # Legger til kunden i databasen
    try:
        cursor.execute('''INSERT INTO Kunde VALUES (?, ?, ?, ?)''',
                       (Kundenummer, Kundenavn, Epost, Mobilnummer))
    except sqlite3.IntegrityError as e:
        print(e)
        print("Kunde finnes allerede med dette mobilnummeret og/eller epostadressen")
        con.close()
        return

    con.commit()
    print("Kunde registrert")

    con.close()
