CREATE TABLE Jernbanestasjon (
    Stasjonsnavn VARCHAR(30), 
    MeterOverHavet INTEGER NOT NULL, 
    CONSTRAINT JernbanestasjonPK PRIMARY KEY (Stasjonsnavn)
);

CREATE TABLE TogruteTabell (
    TogruteTabellID INTEGER PRIMARY KEY,
    TogruteID INTEGER NOT NULL, 
    CONSTRAINT TogruteTabellFK FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE StasjonerITabell (
    Stasjonsnavn VARCHAR(30) NOT NULL,
    TogruteTabellID INTEGER NOT NULL,
    Avgangstid TIME,
    Ankomsttid TIME,
    PRIMARY KEY (Stasjonsnavn, TogruteTabellID),
    CONSTRAINT StasjonerITabellFK1 FOREIGN KEY (Stasjonsnavn) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT StasjonerITabellFK2 FOREIGN KEY (TogruteTabellID) REFERENCES TogruteTabell(TogruteTabellID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TogruteForekomst (
  Ukedag VARCHAR(10),
  TogruteID INTEGER,
  PRIMARY KEY (Ukedag, TogruteID),
  CONSTRAINT TogruteForekomstFK FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Operatør (
    Operatørnavn VARCHAR(30) PRIMARY KEY,
    AntallSittevogner INTEGER NOT NULL,
    AntallSovevogner INTEGER NOT NULL
);

CREATE TABLE Banestrekning (
    Strekningsnavn VARCHAR(30) PRIMARY KEY,
    Fremdriftsenergi VARCHAR(30),
    AntallDelstrekninger INTEGER,
    Startstasjon VARCHAR(30) NOT NULL,
    EndeStasjon VARCHAR(30) NOT NULL,
    CONSTRAINT BanestrekningFK1 FOREIGN KEY (Startstasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT BanestrekningFK2 FOREIGN KEY (EndeStasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Togrute (
    TogruteID INTEGER PRIMARY KEY,
    Retning VARCHAR(30) NOT NULL,
    Startstasjon VARCHAR(30) NOT NULL,
    Endestasjon VARCHAR(30) NOT NULL,
    Operatørnavn VARCHAR(30) NOT NULL,
    Strekningsnavn VARCHAR(30) NOT NULL,
    CONSTRAINT TogruteFK1 FOREIGN KEY (Startstasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT TogruteFK2 FOREIGN KEY (Endestasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT TogruteFK3 FOREIGN KEY (Operatørnavn) REFERENCES Operatør(Operatørnavn)
        ON UPDATE CASCADE ON DELETE SET NULL, 
    CONSTRAINT TogruteFK4 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE Delstrekning (
    StrekningsID INTEGER, 
    Startstasjon VARCHAR(30) NOT NULL,
    EndeStasjon VARCHAR(30) NOT NULL,
    Lengde INTEGER,
    Spor VARCHAR(30),
    Strekningsnavn VARCHAR(30) NOT NULL,
    PRIMARY KEY (StrekningsID, Strekningsnavn),
    CONSTRAINT DelstrekningFK1 FOREIGN KEY (Startstasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT DelstrekningFK2 FOREIGN KEY (EndeStasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT DelstrekningFK3 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE TogruteHarDelstrekning (
    TogruteID INTEGER, 
    StrekningsID INTEGER, 
    Strekningsnavn VARCHAR(30), 
    PRIMARY KEY (TogruteID, StrekningsID, Strekningsnavn), 
    CONSTRAINT TogruteHarDelstrekningFK1 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT TogruteHarDelstrekningFK2 FOREIGN KEY (StrekningsID) REFERENCES Delstrekning(StrekningsID)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT TogruteHarDelstrekningFK3 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE BanestrekningHarStasjoner (
    Stasjonsnavn VARCHAR(30),
    Strekningsnavn VARCHAR(30),
    PRIMARY KEY (Stasjonsnavn, Strekningsnavn),
    CONSTRAINT BanestrekningHarStasjonerFK1 FOREIGN KEY (Stasjonsnavn) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT BanestrekningHarStasjonerFK2 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Vognoppsett (
    VognoppsettID INTEGER,
    AntSittevogner INTEGER NOT NULL,
    AntSovevogner INTEGER NOT NULL,
    TogruteID INTEGER,
    PRIMARY KEY (VognoppsettID, TogruteID),
    CONSTRAINT VognoppsettFK FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE HarVogntyper (
    Operatørnavn VARCHAR(30),
    Vognnavn VARCHAR(30),
    PRIMARY KEY (Operatørnavn, Vognnavn),
    CONSTRAINT HarVogntyperFK1 FOREIGN KEY (Operatørnavn) REFERENCES Operatør(Operatørnavn)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT HarVogntyperFK2 FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE Vogntype (
    Vognnavn VARCHAR(30) PRIMARY KEY,
    Type VARCHAR(30) NOT NULL
);

CREATE TABLE Sovevogn (
    SovevognID INTEGER PRIMARY KEY,
    Vognnavn VARCHAR(30) NOT NULL,
    CONSTRAINT SovevognFK FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE SovevognDesign (
    Vognnavn VARCHAR(30) PRIMARY KEY,
    AntSovekupeer INTEGER NOT NULL,
    CONSTRAINT SovevognDesignFK FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE Sittevogn (
    SittevognID INTEGER PRIMARY KEY, 
    Vognnavn VARCHAR(30) NOT NULL,
    CONSTRAINT SittevognFK FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE SittevognDesign (
    Vognnavn VARCHAR(30) PRIMARY KEY,
    AntStolrader INTEGER NOT NULL,
    AntSeterPrRad INTEGER NOT NULL,
    CONSTRAINT SittevognDesignFK FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE Sete (
    SeteNr INTEGER, 
    SittevognID INTEGER, 
    PRIMARY KEY (SeteNr, SittevognID),
    CONSTRAINT SeteFK FOREIGN KEY (SittevognID) REFERENCES Sittevogn(SittevognID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Kupee (
    KupeeNr INTEGER, 
    SovevognID INTEGER, 
    PRIMARY KEY (KupeeNr, SovevognID),
    CONSTRAINT KupeeFK FOREIGN KEY (SovevognID) REFERENCES Sovevogn(SovevognID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE BestårAv (
    Vognnavn VARCHAR(30),
    VognoppsettID INTEGER,
    TogruteID INTEGER,
    NummerForfra INTEGER, 
    SovevognID INTEGER, 
    SittevognID INTEGER, 
    PRIMARY KEY (Vognnavn, VognoppsettID, TogruteID, NummerForfra),
    CONSTRAINT BestårAvFK1 FOREIGN KEY (Vognnavn) REFERENCES Vogntype(Vognnavn)
        ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT BestårAvFK2 FOREIGN KEY (VognoppsettID) REFERENCES Vognoppsett(VognoppsettID)
        ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT BestårAvFK3 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT BestårAvFK4 FOREIGN KEY (SovevognID) REFERENCES Sovevogn(SovevognID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT BestårAvFK5 FOREIGN KEY (SittevognID) REFERENCES Sittevogn(SittevognID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Kunde (
  Kundenummer INTEGER PRIMARY KEY,
  Kundenavn VARCHAR(30) NOT NULL,
  Epost VARCHAR(30) NOT NULL UNIQUE,
  Mobilnummer INTEGER NOT NULL UNIQUE
);


CREATE TABLE Kundeordre (
  Ordrenummer INTEGER PRIMARY KEY,
  Dato DATE NOT NULL,
  Tid TIME NOT NULL,
  AntallBillettkjøp INTEGER NOT NULL,
  Kundenummer INTEGER NOT NULL, 
  Ukedag VARCHAR(10) NOT NULL, 
  TogruteID INTEGER NOT NULL, 
    CONSTRAINT KundeordreFK1 FOREIGN KEY (Kundenummer) REFERENCES Kunde(Kundenummer)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT KundeordreFK2 FOREIGN KEY (Ukedag) REFERENCES Togruteforekomst(Ukedag)
        ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT KundeordreFK3 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE SeteBillett (
  BillettNr INTEGER,
  BillettDato DATE NOT NULL, 
  Startstasjon VARCHAR(30) NOT NULL,
  Endestasjon VARCHAR(30) NOT NULL,
  SeteNr INTEGER NOT NULL,
  SittevognID INTEGER NOT NULL, 
  Ordrenummer INTEGER, 
    PRIMARY KEY (BillettNr, Ordrenummer), 
    CONSTRAINT SeteBillettFK1 FOREIGN KEY (Startstasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT SeteBillettFK2 FOREIGN KEY (Endestasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL, 
    CONSTRAINT SeteBillettFK3 FOREIGN KEY (SeteNr) REFERENCES Sete(SeteNr)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT SeteBillettFK4 FOREIGN KEY (SittevognID) REFERENCES Sittevogn(SittevognID)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SeteBillettFK5 FOREIGN KEY (Ordrenummer) REFERENCES Kundeordre(Ordrenummer)
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE SeteBillettTilhørerDelstrekning (
  StrekningsID INTEGER, 
  BillettDato DATE, 
  SeteNr INTEGER, 
  SittevognID INTEGER, 
  Strekningsnavn VARCHAR(30), 
  BillettNr INTEGER NOT NULL, 
  Ordrenummer INTEGER NOT NULL,
    PRIMARY KEY (StrekningsID, BillettDato, SeteNr, SittevognID, Strekningsnavn), 
    CONSTRAINT SeteBillettTilhørerDelstrekningFK1 FOREIGN KEY (StrekningsID) REFERENCES Delstrekning(StrekningsID)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SeteBillettTilhørerDelstrekningFK2 FOREIGN KEY (SittevognID) REFERENCES Sittevogn(SittevognID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT SeteBillettTilhørerDelstrekningFK3 FOREIGN KEY (BillettDato) REFERENCES Billett(BillettDato)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT SeteBillettTilhørerDelstrekningFK4 FOREIGN KEY (SeteNr) REFERENCES Sete(SeteNr)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT SeteBillettTilhørerDelstrekningFK5 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SeteBillettTilhørerDelstrekningFK6 FOREIGN KEY (BillettNr) REFERENCES Billett(BillettNr)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT SeteBillettTilhørerDelstrekningFK7 FOREIGN KEY (Ordrenummer) REFERENCES Kundeordre(Ordrenummer)
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE SoveBillett (
  BillettNr INTEGER UNIQUE,
  BillettDato DATE NOT NULL, 
  Startstasjon VARCHAR(30) NOT NULL,
  Endestasjon VARCHAR(30) NOT NULL,
  KupeeNr INTEGER NOT NULL, 
  SovevognID INTEGER NOT NULL,
  Ordrenummer INTEGER, 
    PRIMARY KEY (BillettNr, Ordrenummer), 
    CONSTRAINT SoveBillettFK1 FOREIGN KEY (Startstasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT SoveBillettFK2 FOREIGN KEY (Endestasjon) REFERENCES Jernbanestasjon(Stasjonsnavn)
        ON UPDATE CASCADE ON DELETE SET NULL, 
    CONSTRAINT SoveBillettFK3 FOREIGN KEY (SovevognID) REFERENCES Sovevogn(SovevognID)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettFK4 FOREIGN KEY (KupeeNr) REFERENCES Kupee(KupeeNr)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettFK5 FOREIGN KEY (Ordrenummer) REFERENCES Kundeordre(Ordrenummer)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SoveBillettTilhørerBanestrekning (
  BillettDato DATE, 
  KupeeNr INTEGER, 
  SovevognID INTEGER, 
  Strekningsnavn VARCHAR(30), 
  BillettNr INTEGER NOT NULL, 
  Ordrenummer INTEGER NOT NULL,
    PRIMARY KEY (BillettDato, KupeeNr, SovevognID, Strekningsnavn), 
    CONSTRAINT SoveBillettTilhørerBanestrekningFK1 FOREIGN KEY (Strekningsnavn) REFERENCES Banestrekning(Strekningsnavn)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettTilhørerBanestrekningFK2 FOREIGN KEY (BillettNr) REFERENCES Billett(BillettNr)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettTilhørerBanestrekningFK3 FOREIGN KEY (Ordrenummer) REFERENCES Kundeordre(Ordrenummer)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT SoveBillettTilhørerBanestrekningFK4 FOREIGN KEY (BillettDato) REFERENCES SoveBillett(BillettDato)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettTilhørerBanestrekningFK5 FOREIGN KEY (KupeeNr) REFERENCES Kupee(KupeeNr)
        ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT SoveBillettTilhørerBanestrekningFK6 FOREIGN KEY (SovevognID) REFERENCES Sovevogn(SovevognID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

