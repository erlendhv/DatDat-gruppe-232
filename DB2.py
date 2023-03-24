from python.brukerhistorie_C import brukerhistorie_c
from python.brukerhistorie_D import brukerhistorie_d
from python.brukerhistorie_E import brukerhistorie_e
from python.brukerhistorie_G import brukerhistorie_g
from python.brukerhistorie_H import brukerhistorie_h

# Kjør appen fra denne siden

if __name__ == "__main__":
    while True:
        print("=============================================================")
        print("Velkommen til Togtider AS")
        print("Hva ønsker du å gjøre?")
        print("1. brukerhistorie_c: Se info om togrute innom en stasjon")
        print("2. brukerhistorie_d: Se info om togrute mellom to stasjoner")
        print("3. brukerhistorie_e: Registrering av ny bruker")
        print("4. brukerhistorie_g: Kjøp billett")
        print("5. brukerhistorie_h: Se info om bestillinger")
        print("6. Avslutt")
        valg = input("Skriv inn ditt valg: ")
        if valg == "1":
            brukerhistorie_c()
        elif valg == "2":
            brukerhistorie_d()
        elif valg == "3":
            brukerhistorie_e()
        elif valg == "4":
            brukerhistorie_g()
        elif valg == "5":
            brukerhistorie_h()
        elif valg == "6":
            exit()
        else:
            print("Ugyldig valg")
        print("=============================================================")
