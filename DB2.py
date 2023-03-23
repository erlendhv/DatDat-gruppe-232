from python.brukerhistorie_C import brukerhistorie_c
from python.brukerhistorie_D import brukerhistorie_d
from python.brukerhistorie_E import brukerhistorie_e
from python.brukerhistorie_G import brukerhistorie_g
from python.brukerhistorie_H import brukerhistorie_h

# Kjør appen fra denne siden

if __name__ == "__main__":
    print("Velkommen til Togtider AS")
    print("Hva ønsker du å gjøre?")
    print("1. brukerhistorie_c")
    print("2. brukerhistorie_d")
    print("3. brukerhistorie_e")
    print("4. brukerhistorie_g")
    print("5. brukerhistorie_h")
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
