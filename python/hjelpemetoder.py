import sqlite3
from collections import deque
import re


def findDelstrekning(start_station, end_station):
    '''
        Dette er en hjelpemetode som finner alle delstrekninger mellom to stasjoner. Den gjør det ved hjelp av 
        en bredde-først-søk (BFS) algoritme. Den tar inn startstasjon og endestasjon, og returnerer en liste
        med korteste mulige rute mellom de to stasjonene.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    # create a set to keep track of visited stations
    visited = set()

    # create a queue to store stations to visit
    queue = deque([(start_station, [])])

    # create a list to store all possible routes
    routes = []

    # perform BFS to find all possible routes
    while queue:
        curr_station, curr_route = queue.popleft()
        visited.add(curr_station)

        # if we've reached the end station, add the current route to the list of routes
        if curr_station == end_station:
            routes.append(curr_route + [curr_station])

        # otherwise, add all unvisited stations connected to the current station to the queue
        else:
            cursor.execute(
                "SELECT EndeStasjon FROM Delstrekning WHERE Startstasjon = ?", (curr_station,))
            for next_station in cursor.fetchall():
                if next_station[0] not in visited:
                    queue.append(
                        (next_station[0], curr_route + [curr_station]))

    returnList = []
    try:
        for i in range(1, len(routes[0])):
            cursor.execute(
                "SELECT * FROM Delstrekning WHERE Startstasjon = ? AND EndeStasjon = ?", (routes[0][i - 1], routes[0][i]))
            returnList.append(cursor.fetchall()[0])
    except:
        print("Det finnes ingen delstrekninger mellom disse stasjonene")
        con.close()
        return []

    con.close()

    return returnList

# finner alle togruter som kjøerer mellom en startstasjon og en sluttstasjon


def findTogruteID(startStasjon, sluttStasjon):
    '''
    Dette er en hjelpemetode som finner alle togruter som kjører mellom to stasjoner. Den gjør det ved hjelp av
    funksjonen over for å finne alle delstrekninger mellom to stasjoner, og så sjekker den hvilke togruter som
    har disse delstrekningene.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    if len(delstrekninger) == 0:
        return []
    delstrekningIDList = []
    for i in delstrekninger:
        delstrekningIDList.append(i[0])
    # finner alle togruter
    cursor.execute(
        "SELECT distinct TogruteID FROM Togrute")
    togruteID = cursor.fetchall()
    IDer = []
    for i in togruteID:
        IDer.append(i[0])
    godkjentTogID = []
    # går gjennom alle togruter og sjekker om de har alle delstrekningene
    for i in IDer:
        cursor.execute(
            "SELECT StrekningsID FROM TogruteHarDelstrekning where TogruteID = ?", (i,))
        TogruteHarDelstrekning = cursor.fetchall()
        strekningsIDListTilTogrute = []
        # lager en liste med alle strekningsIDene til togruten
        for x in TogruteHarDelstrekning:
            strekningsIDListTilTogrute.append(x[0])
        # finner snittet mellom togrutens liste over delstrekninger og delstrekningene
        common_list = set(delstrekningIDList).intersection(
            strekningsIDListTilTogrute)
        # hvis snittet er lik lengden på antall delstrekninger, er togruten godkjent
        if len(common_list) == len(delstrekningIDList):
            godkjentTogID.append(i)

    con.close()

    return godkjentTogID


def toWeekday(weekday):
    '''
    Dette er en hjelpemetode som gjør om ukedag i int til ukedag i string.
    '''
    ukedag1 = weekday
    match ukedag1:
        case 0:
            ukedag1 = "mandag"
        case 1:
            ukedag1 = "tirsdag"
        case 2:
            ukedag1 = "onsdag"
        case 3:
            ukedag1 = "torsdag"
        case 4:
            ukedag1 = "fredag"
        case 5:
            ukedag1 = "lørdag"
        case 6:
            ukedag1 = "søndag"
    return ukedag1


def validJernbanestasjon(stasjonsnavnInput):
    '''
    Dette er en hjelpemetode som henter ut alle jernbanestasjonene i databasen.
    Den sjekker så om stasjonsnavnet som brukeren har skrevet inn er gyldig.
    Hvis det er gyldig, returneres stasjonsnavnet. Hvis ikke, får brukeren skrive inn stasjonsnavnet på nytt.
    '''
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    cursor.execute("select Stasjonsnavn from Jernbanestasjon")
    stasjoner = cursor.fetchall()

    stasjonsnavn = []
    for stasjon in stasjoner:
        stasjonsnavn.append(stasjon[0])

    while stasjonsnavnInput not in stasjonsnavn:
        print("Ugyldig stasjonsnavn")
        print("Eksisterende stasjoner: ")
        for stasjon in stasjoner:
            print(stasjon[0])
        stasjonsnavnInput = input("Skriv inn stasjonsnavn på nytt: ")

    con.close()

    return stasjonsnavnInput


def dateCheck(dato):
    '''
    Dette er en hjelpemetode som sjekker om datoen som brukeren har skrevet inn er på gyldig format.
    Den sjekker om det er 4 siffer, bindestrek og 2 siffer, bindestrek og 2 siffer.
    Hvis den er gyldig, returneres datoen. Hvis ikke, får brukeren skrive inn datoen på nytt.
    '''
    date_regex = r'^\d{4}-\d{2}-\d{2}$'
    match = re.match(date_regex, dato)
    while not match:
        print("Feil format på dato. Prøv igjen.")
        dato = input("Angi ønsket dato (YYYY-MM-DD): ")
        match = re.match(date_regex, dato)
    return dato
