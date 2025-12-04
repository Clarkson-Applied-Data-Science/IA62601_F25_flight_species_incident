import csv
import requests
from datetime import datetime, timezone, timedelta
from data_fetcher import fetch_airport_data, fetch_species_data
import global_vars as gv
import json
import pymysql
import yaml
from pathlib import Path
import re
config = yaml.safe_load(Path('config.yml').read_text())
def batch_reader(file_path, batch_size=10):
    with open(file_path, 'r') as f:
        batch = []
        for line in f:
            batch.append(line)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
def connect_to_db():
    conn = pymysql.connect(host=config['db']['host'], port=3306, user=config['db']['user'], passwd=config['db']['pw'], db=config['db']['db'], autocommit=True)
    return conn.cursor(pymysql.cursors.DictCursor)

def populate_table_species(tokens):
    cur = connect_to_db()  
    col =['species_name','class']
    sql = f"""
            INSERT INTO {config['tables']['species']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens) 

def species_kingdom_aligner():
    count_higher_category = {}
    isheader = True
    species_list=[]
    for batch in batch_reader(gv.SPECIES_PATH, batch_size=5000): 
        for line in batch:
            if isheader:
                    isheader = False
                    continue
            row = next(csv.reader([line]))
            key = row[0]    
            val = row[7]   
            single_counter = count_higher_category.setdefault(key, {})
            single_counter[val] = single_counter.get(val, 0) + 1
    for species, counts in count_higher_category.items(): 
        best_class = max(counts, key=counts.get)
        species_list.append((species,best_class))
        #best_class_by_species[species] = best_class
    populate_table_species(species_list)
species_kingdom_aligner()

def populate_table_airlines(tokens):
    cur = connect_to_db()  
    col =['airline', 'icao']
    sql = f"""
            INSERT INTO {config['tables']['airline']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)

def populate_table_airports(tokens):
    cur = connect_to_db()  
    #col =['name','city','country','icao','iata'	,'latitude_deg','longitude_deg','elevation_ft'	]
    col =['name','icao'	]
    sql = f"""
            INSERT INTO {config['tables']['airport']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)

airport_set = set()   
airlines_set = set() 
isheader = True 
for batch in batch_reader(gv.RAW_DATABASE_PATH, batch_size=5000):
    airport_db = []   
    airlines_db = []
    for line in batch:
        if isheader:
            isheader = False
            continue
        row = next(csv.reader([line])) 
        airport_icao = row[19].strip()
        airline_icao = row[4].strip() 
        if airport_icao not in airport_set and re.fullmatch(r'[A-Za-z]{4}', airport_icao):
            airport_set.add(airport_icao)
            airport_db.append((
                row[20], airport_icao
            ))
        if airline_icao not in airlines_set and re.fullmatch(r'[A-Za-z]{3}', airline_icao):
            airlines_set.add(airline_icao)
            airlines_db.append((
                row[5], airline_icao
            ))
    populate_table_airlines(airlines_db)
    populate_table_airports(airport_db)

def populate_table_flight(tokens):
    cur = connect_to_db()  
    col =['full_code','aid']
    sql = f"""
            INSERT INTO {config['tables']['flight']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)

def populate_table_incident(tokens):
    cur = connect_to_db()  
    col =['full_code','aid']
    sql = f"""
            INSERT INTO {config['tables']['incident']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)


