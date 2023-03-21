import sqlite3
from python.brukerhistorie_C import brukerhistorie_c
from python.brukerhistorie_D import brukerhistorie_d
from python.brukerhistorie_E import brukerhistorie_e
from python.brukerhistorie_G import brukerhistorie_g
from python.brukerhistorie_H import brukerhistorie_h

# con = sqlite3.connect('232DB.db')
# cursor = con.cursor()


if __name__ == "__main__":
    print("Velkommen til Togtider AS")
    # brukerhistorie_d()
    # brukerhistorie_c()
    brukerhistorie_e()

    # cursor.execute(
    #     "SELECT * FROM Kundeordre")
    # kundeordre = cursor.fetchall()
    # print("Kundeordre")
    # print(kundeordre)
    # cursor.execute(
    #     "SELECT * FROM SeteBillett")
    # setebillett = cursor.fetchall()
    # print("Setebillett")
    # print(setebillett)
    # cursor.execute(
    #     "SELECT * FROM SoveBillett")
    # sovebillett = cursor.fetchall()
    # print("Sovebillett")
    # print(sovebillett)
    # cursor.execute(
    #     "SELECT * FROM SetebillettTilhørerDelstrekning")
    # setebillettTilhørerDelstrekning = cursor.fetchall()
    # print("SetebillettTilhørerDelstrekning")
    # print(setebillettTilhørerDelstrekning)
    # cursor.execute(
    #     "SELECT * FROM SovebillettTilhørerBanestrekning")
    # sovebillettTilhørerBanestrekning = cursor.fetchall()
    # print("SovebillettTilhørerBanestrekning")
    # print(sovebillettTilhørerBanestrekning)

# con.close()
