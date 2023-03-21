import sqlite3
from collections import deque


def brukerhistorie_e():
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    Kundenummer = 0
    cursor.execute("select Kundenummer from Kunde order by Kundenummer asc")
    Kundenummer1 = cursor.fetchall()

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
