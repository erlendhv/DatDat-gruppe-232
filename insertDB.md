#Brukerhistorie a og b

#Jernbanestasjon
insert into Jernbanestasjon values ("Trondheim S", 5.1);
insert into Jernbanestasjon values ("Steinkjer", 3.6);
insert into Jernbanestasjon values ("Mosjøen", 6.8);
insert into Jernbanestasjon values ("Mo i Rana", 3.5);
insert into Jernbanestasjon values ("Fauske", 34);
insert into Jernbanestasjon values ("Bodø", 4.1);

#Banestrekning
insert into Banestrekning values ("Nordlandsbanen", "Diesel", 5, "Trondheim S", "Bodø");

#BanestrekningHarStasjoner
insert into BanestrekningHarStasjoner values ("Trondheim S", "Nordlandsbanen");
insert into BanestrekningHarStasjoner values ("Steinkjer", "Nordlandsbanen");
insert into BanestrekningHarStasjoner values ("Mosjøen", "Nordlandsbanen");
insert into BanestrekningHarStasjoner values ("Mo i Rana", "Nordlandsbanen");
insert into BanestrekningHarStasjoner values ("Fauske", "Nordlandsbanen");
insert into BanestrekningHarStasjoner values ("Bodø", "Nordlandsbanen");

#Delstrekning
insert into Delstrekning values (1, "Trondheim S", "Steinkjer", 120, "Dobbel", "Nordlandsbanen");
insert into Delstrekning values (2, "Steinkjer", "Mosjøen", 280, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (3, "Mosjøen", "Mo i Rana", 90, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (4, "Mo i Rana", "Fauske", 170, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (5, "Fauske", "Bodø", 60, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (6, "Bodø", "Fauske", 60, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (7, "Fauske", "Mo i Rana", 170, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (8, "Mo i Rana", "Mosjøen", 90, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (9, "Mosjøen", "Steinkjer", 280, "Enkel", "Nordlandsbanen");
insert into Delstrekning values (10, "Steinkjer", "Trondheim S", 120, "Dobbel", "Nordlandsbanen");

#Operatør
insert into Operatør values ("SJ", 4, 1);

#Togrute
insert into Togrute values (1, "I", "Trondheim S", "Bodø", "SJ", "Nordlandsbanen");
insert into Togrute values (2, "I", "Trondheim S", "Bodø", "SJ", "Nordlandsbanen");
insert into Togrute values (3, "Mot", "Mo i Rana", "Trondheim S", "SJ", "Nordlandsbanen");

#TogruteHarDelstrekning
insert into TogruteHarDelstrekning values (1, 1, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 2, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 3, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 4, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (1, 5, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 1, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 2, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 3, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 4, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (2, 5, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (3, 8, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (3, 9, "Nordlandsbanen");
insert into TogruteHarDelstrekning values (3, 10, "Nordlandsbanen");

#TogruteTabell
insert into TogruteTabell values (1, 1);
insert into TogruteTabell values (2, 2);
insert into TogruteTabell values (3, 3);

#StasjonerITabell
insert into StasjonerITabell values ("Trondheim S", 1, "07:49:00", null);
insert into StasjonerITabell values ("Steinkjer", 1, "09:51:00", "09:51:00");
insert into StasjonerITabell values ("Mosjøen", 1, "13:20:00", "13:20:00");
insert into StasjonerITabell values ("Mo i Rana", 1, "14:31:00", "14:31:00");
insert into StasjonerITabell values ("Fauske", 1, "16:49:00", "16:49:00");
insert into StasjonerITabell values ("Bodø", 1, null, "17:34:00");
insert into StasjonerITabell values ("Trondheim S", 2, "23:05:00", null);
insert into StasjonerITabell values ("Steinkjer", 2, "00:57:00", "00:57:00");
insert into StasjonerITabell values ("Mosjøen", 2, "04:41:00", "04:41:00");
insert into StasjonerITabell values ("Mo i Rana", 2, "05:55:00", "05:55:00");
insert into StasjonerITabell values ("Fauske", 2, "08:19:00", "08:19:00");
insert into StasjonerITabell values ("Bodø", 2, null, "09:05:00");
insert into StasjonerITabell values ("Mo i Rana", 3, "08:11:00", null);
insert into StasjonerITabell values ("Mosjøen", 3, "09:14:00", "09:14:00");
insert into StasjonerITabell values ("Steinkjer", 3, "12:31:00", "12:31:00");
insert into StasjonerITabell values ("Trondheim S", 3, null, "14:13:00");

#TogruteForekomst
insert into TogruteForekomst values ("Mandag", 1);
insert into TogruteForekomst values ("Tirsdag", 1);
insert into TogruteForekomst values ("Onsdag", 1);
insert into TogruteForekomst values ("Torsdag", 1);
insert into TogruteForekomst values ("Fredag", 1);
insert into TogruteForekomst values ("Mandag", 2);
insert into TogruteForekomst values ("Tirsdag", 2);
insert into TogruteForekomst values ("Onsdag", 2);
insert into TogruteForekomst values ("Torsdag", 2);
insert into TogruteForekomst values ("Fredag", 2);
insert into TogruteForekomst values ("Lørdag", 2);
insert into TogruteForekomst values ("Søndag", 2);
insert into TogruteForekomst values ("Mandag", 3);
insert into TogruteForekomst values ("Tirsdag", 3);
insert into TogruteForekomst values ("Onsdag", 3);
insert into TogruteForekomst values ("Torsdag", 3);
insert into TogruteForekomst values ("Fredag", 3);

#Vogntype
insert into Vogntype values ("SJ-sittevogn-1", "Sittevogn");
insert into Vogntype values ("SJ-sovevogn-1", "Sovevogn");

#Sovevogn
insert into Sovevogn values (1, "SJ-sovevogn-1");

#SovevognDesign
insert into SovevognDesign values ("SJ-sovevogn-1", 4);

#Sittevogn
insert into Sittevogn values (1, "SJ-sittevogn-1");
insert into Sittevogn values (2, "SJ-sittevogn-1");
insert into Sittevogn values (3, "SJ-sittevogn-1");
insert into Sittevogn values (4, "SJ-sittevogn-1");

#SittevognDesign
insert into SittevognDesign values ("SJ-sittevogn-1", 3, 4);

#HarVognTyper
insert into HarVognTyper values ("SJ", "SJ-sittevogn-1");
insert into HarVognTyper values ("SJ", "SJ-sovevogn-1");

#Sete
insert into Sete values (1, 1);
insert into Sete values (2, 1);
insert into Sete values (3, 1);
insert into Sete values (4, 1);
insert into Sete values (5, 1);
insert into Sete values (6, 1);
insert into Sete values (7, 1);
insert into Sete values (8, 1);
insert into Sete values (9, 1);
insert into Sete values (10, 1);
insert into Sete values (11, 1);
insert into Sete values (12, 1);

insert into Sete values (1, 2);
insert into Sete values (2, 2);
insert into Sete values (3, 2);
insert into Sete values (4, 2);
insert into Sete values (5, 2);
insert into Sete values (6, 2);
insert into Sete values (7, 2);
insert into Sete values (8, 2);
insert into Sete values (9, 2);
insert into Sete values (10, 2);
insert into Sete values (11, 2);
insert into Sete values (12, 2);

insert into Sete values (1, 3);
insert into Sete values (2, 3);
insert into Sete values (3, 3);
insert into Sete values (4, 3);
insert into Sete values (5, 3);
insert into Sete values (6, 3);
insert into Sete values (7, 3);
insert into Sete values (8, 3);
insert into Sete values (9, 3);
insert into Sete values (10, 3);
insert into Sete values (11, 3);
insert into Sete values (12, 3);

insert into Sete values (1, 4);
insert into Sete values (2, 4);
insert into Sete values (3, 4);
insert into Sete values (4, 4);
insert into Sete values (5, 4);
insert into Sete values (6, 4);
insert into Sete values (7, 4);
insert into Sete values (8, 4);
insert into Sete values (9, 4);
insert into Sete values (10, 4);
insert into Sete values (11, 4);
insert into Sete values (12, 4);

#Kupee
insert into Kupee values (1, 1);
insert into Kupee values (2, 1);
insert into Kupee values (3, 1);
insert into Kupee values (4, 1);

#Vognoppsett
insert into Vognoppsett values (1, 2, 0, 1);
insert into Vognoppsett values (2, 1, 1, 2);
insert into Vognoppsett values (3, 1, 0, 3);

#BestårAv
insert into BestårAv values ("SJ-sittevogn-1", 1, 1, 1, null, 1);
insert into BestårAv values ("SJ-sittevogn-1", 1, 1, 2, null, 2);
insert into BestårAv values ("SJ-sitteevogn-1", 2, 2, 1, null, 3);
insert into BestårAv values ("SJ-sovevogn-1", 2, 2, 2, 1, null);
insert into BestårAv values ("SJ-sittevogn-1", 3, 3, 1, null, 4);
