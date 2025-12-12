import csv
from datetime import datetime
from tools import config, connect_to_db, batch_reader, str_to_float_convertor, str_to_int_convertor
import global_vars as gv
import re
import json
flight_set = {}
airport_set = {}
aircraft_set = {}
airlines_set = {}
species_set = {}


def truncate(tables):
    cur = connect_to_db()
    for table in tables:
        sql = f"TRUNCATE TABLE `{table}`;"
        cur.execute(sql)


def populate_table_species(tokens):
    cur = connect_to_db()
    col = ['species_name', 'class']
    sql = f"""
            INSERT INTO {config['tables']['species']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)
    species_index = col.index('species_name')
    species_values = [row[species_index] for row in tokens]
    if not species_values:
        return []

    placeholders = ','.join(['%s'] * len(species_values))
    sql = f"""
            SELECT sid, species_name FROM {config['tables']['species']}
            WHERE species_name IN ({placeholders});
            """
    cur.execute(sql, species_values)
    return cur.fetchall()


def cleaning_unknown():
    is_header = True
    with open(gv.CLEANED_DATABASE_PATH, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        for batch in batch_reader(gv.RAW_DATABASE_PATH, batch_size=gv.BATCH_SIZE):
            for line in batch:
                row = next(csv.reader([line]))
                if is_header:
                    writer.writerow(row)
                    is_header = False
                    continue
                operator_id = row[4].strip().upper()
                operator = row[5].strip().upper()
                aircraft = row[6].strip().upper()
                airport = row[20].strip().upper()
                species_id = row[30].strip().upper()

                if (
                    operator_id in ("", "UNK", "UNKNOWN")
                    or operator in ("", "UNK", "UNKNOWN")
                    or aircraft in ("", "UNK", "UNKNOWN")
                    or airport in ("", "UNK", "UNKNOWN")
                    or species_id in ("", "UNK", "UNKNOWN")
                ):
                    continue
                writer.writerow(row)


def species_kingdom_aligner():
    count_higher_category = {}
    isheader = True
    species_list = []
    species_seen = set()
    for batch in batch_reader(gv.SPECIES_PATH, batch_size=gv.BATCH_SIZE):
        for line in batch:
            if isheader:
                isheader = False
                continue
            row = next(csv.reader([line]))

            species_name_ = row[0]
            class_ = row[7]
            single_counter = count_higher_category.setdefault(
                species_name_, {})
            single_counter[class_] = single_counter.get(class_, 0) + 1
    for species, counts in count_higher_category.items():
        best_class = max(counts, key=counts.get)
        if species not in species_seen:
            species_list.append((species, best_class))
            species_seen.add(species)
        # best_class_by_species[species] = best_class
    species_db = populate_table_species(species_list)
    species_set.update({row["species_name"]: row["sid"] for row in species_db})


def populate_table_flight(tokens):
    cur = connect_to_db()
    col = ['full_code', 'aid']
    sql = f"""
            INSERT INTO {config['tables']['flight']} ({','.join(col)})
            VALUES (%s, %s);
            """
    cur.executemany(sql, tokens)
    placeholders = ','.join(['%s'] * len(tokens))
    sql = f"""
            SELECT fid, full_code FROM {config['tables']['flight']}
            WHERE full_code IN ({placeholders});
            """
    cur.execute(sql, tokens)
    return cur.fetchall()


def populate_table_airports(tokens):
    cur = connect_to_db()
    col = ['name', 'icao', 'latitude_deg',
           'longitude_deg', "city_code", "country"]
    sql = f"""
            INSERT INTO {config['tables']['airport']} ({','.join(col)})
            VALUES ({','.join(['%s'] * len(col))});
            """
    cur.executemany(sql, tokens)
    icao_index = col.index('icao')
    icao_values = [row[icao_index] for row in tokens]
    if not icao_values:
        return []

    placeholders = ','.join(['%s'] * len(icao_values))
    sql = f"""
            SELECT aid, icao FROM {config['tables']['airport']}
            WHERE icao IN ({placeholders});
            """
    cur.execute(sql, icao_values)
    return cur.fetchall()


def populate_table_aircraft(tokens):
    cur = connect_to_db()
    col = ['type', 'mass', 'manufacturer',
           'model_family', 'variant', 'aircraft']
    sql = f"""
            INSERT INTO {config['tables']['aircraft']} ({','.join(col)})
            VALUES ({','.join(['%s'] * len(col))});
            """
    cur.executemany(sql, tokens)
    aircraft_index = col.index('aircraft')
    aircraft_values = [row[aircraft_index] for row in tokens]
    if not aircraft_values:
        return []

    placeholders = ','.join(['%s'] * len(aircraft_values))
    sql = f"""
            SELECT plane_id, aircraft  FROM {config['tables']['aircraft']}
            WHERE aircraft IN ({placeholders});
            """
    cur.execute(sql, aircraft_values)
    return cur.fetchall()


def populate_table_airlines(tokens):
    cur = connect_to_db()
    col = ['airline', 'icao']  # , 'callsign', 'country']
    sql = f"""
            INSERT INTO {config['tables']['airline']} ({','.join(col)})
            VALUES ({','.join(['%s'] * len(col))});
            """
    cur.executemany(sql, tokens)
    icao_index = col.index('icao')
    icao_values = [row[icao_index] for row in tokens]
    if not icao_values:
        return []

    placeholders = ','.join(['%s'] * len(icao_values))
    sql = f"""
            SELECT aid, icao  FROM {config['tables']['airline']}
            WHERE icao IN ({placeholders});
            """
    cur.execute(sql, icao_values)
    return cur.fetchall()


def populate_table_incident(tokens):
    cur = connect_to_db()
    col = ['record_id', 'incident_date', 'operator_id', 'aircraft_id', 'airport_id', 'flight_phase', 'visibility',
           'precipitation', 'height', 'speed', 'distance', 'species_id', 'species_quantity']
    sql = f"""
            INSERT INTO {config['tables']['incident']} ({','.join(col)})
            VALUES ({','.join(['%s'] * len(col))});
            """
    cur.executemany(sql, tokens)


def main():
    truncate([
        config['tables']['incident'],
        config['tables']['airline'],
        config['tables']['aircraft'],
        config['tables']['airport'],
        config['tables']['flight'],
        config['tables']['species'],
    ])
    isheader = True
    cleaning_unknown()
    species_kingdom_aligner()
    with open(gv.AIRPORT_LOCATION_PATH, encoding="utf-8") as f:
        airport_locations = json.load(f)
    for batch in batch_reader(gv.CLEANED_DATABASE_PATH, batch_size=gv.BATCH_SIZE):
        flight_db = []
        airport_db = []
        aircraft_db = []
        airlines_db = []
        incident_db = []
        for line in batch:
            if isheader:
                isheader = False
                continue
            row = next(csv.reader([line]))
            airport_icao = row[19].strip()
            airline_icao = row[4].strip()
            aircraft_id = row[6]
            if row[31] not in species_set or not re.fullmatch(r'[A-Za-z]{4}', airport_icao) or not re.fullmatch(r'[A-Za-z]{3}', airline_icao):
                continue
            if airport_icao not in airport_set:
                airport_set[airport_icao] = None
                airport_db.append((
                    row[20], airport_icao,
                    airport_locations.get(airport_icao, {}).get("latitude"),
                    airport_locations.get(airport_icao, {}).get("longitude"),
                    airport_locations.get(airport_icao, {}).get("city"),
                    airport_locations.get(airport_icao, {}).get("country"),
                ))
            if aircraft_id not in aircraft_set:
                aircraft_set[aircraft_id] = None
                val = row[6]
                parts = str(val).split('-')
                parts += [None] * (3 - len(parts))
                aircraft_db.append((
                    row[7], row[10], parts[0], row[9], parts[1], aircraft_id
                ))
            if airline_icao not in airlines_set:
                airlines_set[airline_icao] = None
                airlines_db.append((
                    row[5], airline_icao
                ))

        airport_db = populate_table_airports(airport_db)
        airport_set.update({row["icao"]: row["aid"] for row in airport_db})

        aircraft_db = populate_table_aircraft(aircraft_db)
        aircraft_set.update({row["aircraft"]: row["plane_id"]
                            for row in aircraft_db})

        airlines_db = populate_table_airlines(airlines_db)
        airlines_set.update({row["icao"]: row["aid"] for row in airlines_db})

        isheader = True
        for line in batch:
            if isheader:
                isheader = False
                continue
            row = next(csv.reader([line]))
            airport_icao = row[19].strip()
            airline_icao = row[4].strip()
            aircraft_id = row[6]
            if row[31] not in species_set or not re.fullmatch(r'[A-Za-z]{4}', airport_icao) or not re.fullmatch(r'[A-Za-z]{3}', airline_icao):
                continue

            aircraft_id = aircraft_set[row[6]]
            airport_id = airport_set[row[19]]
            distance = str_to_float_convertor(row[29])
            flight_phase = row[24]
            height = str_to_float_convertor(row[27])
            incident_date = '/'.join([row[3], row[2], row[1]])
            incident_date = datetime.strptime(incident_date, "%d/%m/%Y")
            operator_id = airlines_set[row[4]]
            precipitation = row[26]
            record_id = row[0]
            species_id = species_set[row[31]]
            species_quantity = row[32]
            speed = str_to_float_convertor(row[28])
            visibility = row[25]

            incident_db.append([record_id, incident_date, operator_id, aircraft_id, airport_id, flight_phase, visibility,
                                precipitation, height, speed, distance, species_id, species_quantity])
        populate_table_incident(incident_db)


if __name__ == "__main__":
    main()
