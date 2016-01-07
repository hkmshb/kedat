"""
Helper scripts for KEDCO's GridIX (Grid Information eXplorer) android 
application.
"""
import os
import sqlite3


def create_dbstruct(cursor):
    script = """
        -- modify SQLite operations/behaviors
        PRAGMA foreign_keys = ON;
        
        CREATE TABLE VoltageRatio (
            Id           INTEGER PRIMARY KEY
          , Value        NVARCHAR(9) NOT NULL UNIQUE
          , Deleted      BOOLEAN NOT NULL DEFAULT(0)
          , DateCreated  DATE NOT NULL DEFAULT(DATE('now'))
          , LastUpdated  DATE NULL
        );
        
        CREATE TABLE TransformerRating (
            Id              INTEGER PRIMARY KEY
          , Code            NVARCHAR(5) NOT NULL UNIQUE
          , Capacity        INTEGER NOT NULL
          , VoltageRatioId  INTEGER NOT NULL
          , Deleted         BOOLEAN NOT NULL DEFAULT(0)
          , DateCreated     DATE NOT NULL DEFAULT(DATE('now'))
          , LastUpdated     DATE NULL
          , CONSTRAINT UX_TRating_Capacity_VoltageRatioId 
                UNIQUE (Capacity, VoltageRatioId)
          , CONSTRAINT FK_TRating_VoltageRatioId_VoltageRatio 
                FOREIGN KEY (VoltageRatioId)
                REFERENCES VoltageRatio(Id)
                ON DELETE RESTRICT ON UPDATE CASCADE
        );
        
        CREATE TABLE Station (
            Id                  INTEGER PRIMARY KEY
          , Code                NVARCHAR(10) NOT NULL UNIQUE
          , Name                NVARCHAR(100) NOT NULL
          , Type                NCHAR(1) NOT NULL
          , IsDedicated         BOOLEAN NOT NULL DEFAULT(0)
          , VoltageRatioId      INTEGER NOT NULL
          , SourceFeederId      INTEGER NULL
          , Address             NVARCHAR(100)
          , City                NVARCHAR(25) NOT NULL
          , State               NVARCHAR(25) NOT NULL
          , DateCommissioned    Date NULL
          , Deleted             BOOLEAN NOT NULL DEFAULT(0)
          , DateCreated         DATE NOT NULL DEFAULT(DATE('now'))
          , LastUpdated         DATE NULL
          , CONSTRAINT CK_Station_Type
                CHECK (Type In ('T', 'I', 'D'))
          , CONSTRAINT FK_Station_VotageRatioId_VoltageRatio
                FOREIGN KEY (VoltageRatioId)
                REFERENCES VoltageRatio(Id)
                ON DELETE RESTRICT ON UPDATE CASCADE
        );
        
        CREATE TABLE Transformer (
            Id                INTEGER PRIMARY KEY
          , Code              NVARCHAR(3) NOT NULL
          , TfmrRatingCode    NVARCHAR(5) NOT NULL
          , StationCode       NVARCHAR(10)
          , SerialNo          NVARCHAR(100)
          , Model             NVARCHAR(100)
          , ManufacturerId    INTEGER NULL
          , Condition         CHAR(1) NOT NULL
          , DateInstalled     DATE NULL
          , DateManufactured  DATE NULL
          , Deleted           BOOLEAN NOT NULL DEFAULT(0)
          , DateCreated       DATE NOT NULL DEFAULT(DATE('now'))
          , LastUpdated       DATE NULL
          , CONSTRAINT UX_Tfmr_Code UNIQUE(Code)
          , CONSTRAINT FK_Tfmr_TfmrRatingCode_TfmrRating
                FOREIGN KEY (TfmrRatingCode)
                REFERENCES TransformerRating(Code)
                ON DELETE RESTRICT ON UPDATE CASCADE
          , CONSTRAINT FK_Tfmr_StationCode_Station
                FOREIGN KEY (StationCode)
                REFERENCES Station(Code)
                ON DELETE RESTRICT ON UPDATE CASCADE
          , CONSTRAINT CK_Tfmr_Condition
                CHECK (Condition In ('U', 'O', 'F', 'D'))
                -- 0: Unknown, 1: OK, 2: Faulty, 3: Damaged
        );
        
      --+===================================================================
      --| TABLE VALUES
      --+===================================================================
        INSERT INTO VoltageRatio (Id, Value)
        VALUES (1, '330/132KV'), (2,   '132/33KV'), (3,   '132/11KV'),
               (4,   '33/11KV'), (5, '33/0.415KV'), (6, '11/0.415KV');
        
        INSERT INTO TransformerRating (Id, Code, Capacity, VoltageRatioId)
        VALUES (1, 'T360M', 60000, 2), (2, 'T340M', 40000, 2), 
               (3, 'T330M', 30000, 2), (4, 'T315M', 15000, 2), 
               (5, 'T375m',  7500, 2), (6, 'T350m',  5000, 2),
               -- injection
               ( 7, 'I115M', 15000, 3), ( 8, 'I112M', 12000, 3), 
               ( 9, 'I175m',  7500, 3), (10, 'I135m',  3500, 3), 
               (11, 'I125m',  2500, 3), (12, 'I116m',  1600, 3),
               (13, 'I110m',  1000, 3);
    """
    cursor.executescript(script)
    print('Db Structure Created...')


def insert_sample_values(cursor):
    script = """
        -- transmission stations
        INSERT INTO Station (Code, Name, Type, IsDedicated, VoltageRatioId, City, State)
        VALUES ('TS01', 'Kumbotso',       'T', 0, 2, 'Kano', 'Kano'),
               ('TS02', 'Dan Agundi',     'T', 0, 2, 'Kano', 'Kano'),
               ('TS03', 'Dakata',         'T', 0, 2, 'Kano', 'Kano'),
               ('TS04', 'Konar Dangora',  'T', 0, 2, 'Kano', 'Kano'),
               ('TS05', 'Hadejia',        'T', 0, 2, 'Hadejia', 'Jigawa'),
               ('TS06', 'Dutse',          'T', 0, 2, 'Dutse', 'Jigawa'),
               ('TS07', 'Kankiya',        'T', 0, 2, 'Katsina', 'Katsina'),
               ('TS08', 'Katsina',        'T', 0, 2, 'Katsina', 'Katsina'),
               ('TS09', 'Funtua',         'T', 0, 2, 'Funtua', 'Katsina');
        
        -- insert transformers
        INSERT INTO Transformer (Code, TfmrRatingCode, StationCode, Condition)
        VALUES ('TR1', 'T330M', 'TS01', 1),
               ('TR2', 'T360M', 'TS01', 1),
               ('TR1', 'T360M', 'TS02', 1),
               ('TR3', 'T360M', 'TS02', 1);
    """
    cursor.executescript(script)
    print('Sample values inserted...')

def create_db():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_dir = os.path.join(base_dir, '..', 'databases')
    db_path = os.path.join(db_dir, 'gridix.sqlite')
    
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    create_dbstruct(conn.cursor())
    insert_sample_values(conn.cursor())
    print('Done!')


