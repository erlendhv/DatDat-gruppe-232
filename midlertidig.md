insert into Delstrekning values (11, "Trondheim S", "Mosjøen", 400, "Begge", "Nordlandsbanen");
insert into Delstrekning values (12, "Trondheim S", "Mo i Rana", 490, "Begge", "Nordlandsbanen");
insert into Delstrekning values (13, "Trondheim S", "Fauske", 660, "Begge", "Nordlandsbanen");
insert into Delstrekning values (14, "Trondheim S", "Bodø", 720, "Begge", "Nordlandsbanen");
insert into Delstrekning values (15, "Steinkjer", "Mo i Rana", 370, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (16, "Steinkjer", "Fauske", 540, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (17, "Steinkjer", "Bodø", 600, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (18, "Mosjøen", "Fauske", 260, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (19, "Mosjøen", "Bodø", 320, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (20, "Mo i Rana", "Bodø", 230, "Enkel", "Nordlandsbanen");

insert into Delstrekning values (21, "Bodø", "Mo i Rana", 230, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (22, "Bodø", "Mosjøen", 320, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (23, "Bodø", "Steinkjer", 600, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (24, "Bodø", "Trondheim S", 720, "Begge", "Nordlandsbanen");
insert into Delstrekning values (25, "Fauske", "Mosjøen", 170, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (26, "Fauske", "Steinkjer", 540, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (27, "Fauske", "Trondheim S", 660, "Begge", "Nordlandsbanen");
insert into Delstrekning values (28, "Mo i Rana", "Steinkjer", 370, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (29, "Mo i Rana", "Trondheim S", 490, "Begge", "Nordlandsbanen");
insert into Delstrekning values (30, "Mosjøen", "Trondheim S", 400, "Begge", "Nordlandsbanen");

insert into TogruteHarDelstrekning values (1, 11, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 12, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 13, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 14, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 15, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 16, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 17, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 18, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 19, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 20, "Nordlandsbanen");

insert into TogruteHarDelstrekning values (2, 11, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 12, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 13, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 14, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 15, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 16, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 17, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 18, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 19, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 20, "Nordlandsbanen");

insert into TogruteHarDelstrekning values (3, 28, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (3, 29, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (3, 30, "Nordlandsbanen");

    # Midlertidig
    # cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
    #     (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
    #         tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
    #             Ukedag = ?) AND Startstasjon = ? AND Sluttstasjon = ? \
    #     AND Avgangstid >= ? ORDER BY Klokkeslett", (ukedag1, ukedag2, startStasjon, sluttStasjon, klokkeslett))
    # resultat = cursor.fetchall()
    # print(resultat)

    # cursor.execute("SELECT tf.TogruteID FROM (TogruteForekomst AS tf JOIN \
    #     (StasjonerITabell AS st JOIN Togrutetabell as tt ON st.TogruteTabellID = \
    #         tt.TogruteTabellID JOIN Togrute as tr ON tr.TogruteID = tt.TogruteID) ON tt.TogruteID = tf.TogruteID) WHERE (Ukedag = ? OR \
    #             Ukedag = ?) AND Startstasjon = ? AND Sluttstasjon = ? \
    #     AND Avgangstid >= ? ORDER BY Klokkeslett", (ukedag1, ukedag2, startStasjon, sluttStasjon, klokkeslett))
    # resultat = cursor.fetchall()
    # print(resultat)



    # cursor.execute('''select Startstasjon, Endestasjon, Avgangstid, TogruteID, Ukedag from StasjonerITabell join
    # (select TogruteTabellID as TabellID, TogruteID, Ukedag, Startstasjon, EndeStasjon from TogruteTabell natural join
    # (select * from TogruteForekomst natural join (select * from TogruteHarDelstrekning natural join
    # (select * from Delstrekning where Startstasjon = ? and EndeStasjon = ?))
    # where Ukedag = ? or Ukedag = ?)) on TabellID = TogruteTabellID and Startstasjon = Stasjonsnavn
    # where Avgangstid >= ?''', (startStasjon, sluttStasjon, ukedag1, ukedag2, klokkeslett))

    # avgangs = cursor.fetchall()
    # print(avgangs)

insert into SeteBillettTilhørerDelstrekning values (2023-)

    avgangs = []
    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join
        (select * from TogruteTabell natural join
        (select * from TogruteForekomst where Ukedag = ?))
        where Avgangstid >= ? and Stasjonsnavn = ?''', (ukedag1, klokkeslett, startStasjon))
    cursor.execute(
        '''select Stasjonsnavn, Avgangstid, TogruteID, Ukedag from StasjonerITabell natural join
        (select * from TogruteTabell natural join
        (select * from TogruteForekomst where Ukedag = ?))
        where Stasjonsnavn = ?''', (ukedag2, startStasjon))
    avgangs = cursor.fetchall()
