import sqlite3
from collections import deque


def findDelstrekning(start_station, end_station):
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
    con = sqlite3.connect('232DB.db')
    cursor = con.cursor()

    delstrekninger = findDelstrekning(startStasjon, sluttStasjon)
    if len(delstrekninger) == 0:
        return []
    delstrekningIDFint = []
    for i in delstrekninger:
        delstrekningIDFint.append(i[0])
    cursor.execute(
        "SELECT distinct TogruteID FROM Togrute")
    togruteID = cursor.fetchall()
    IDer = []
    for i in togruteID:
        IDer.append(i[0])
    godkjentTogID = []
    for i in IDer:
        cursor.execute(
            "SELECT StrekningsID FROM TogruteHarDelstrekning where TogruteID = ?", (i,))
        TogruteHarDelstrekning = cursor.fetchall()
        penListe = []
        for x in TogruteHarDelstrekning:
            penListe.append(x[0])
        common_list = set(delstrekningIDFint).intersection(penListe)
        if len(common_list) == len(delstrekningIDFint):
            godkjentTogID.append(i)

    con.close()

    return godkjentTogID

# Gjør om ukedag som nå er int til Mandag, Tirsdag osv.


def toWeekday(weekday):
    ukedag1 = weekday
    match ukedag1:
        case 0:
            ukedag1 = "Mandag"
        case 1:
            ukedag1 = "Tirsdag"
        case 2:
            ukedag1 = "Onsdag"
        case 3:
            ukedag1 = "Torsdag"
        case 4:
            ukedag1 = "Fredag"
        case 5:
            ukedag1 = "Lørdag"
        case 6:
            ukedag1 = "Søndag"
    return ukedag1
