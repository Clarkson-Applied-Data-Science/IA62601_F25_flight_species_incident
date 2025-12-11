import requests
import pandas as pd
import csv
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tools import config, connect_to_db, batch_reader, str_to_float_convertor, str_to_int_convertor
import global_vars as gv
from tools import config
FIELDNAMES = [
    "input_name", "usageKey", "scientificName", "canonicalName",
    "rank", "kingdom", "phylum", "class", "order", "family",
    "genus", "species", "taxonomicStatus"
]
headers = {"Accept": "application/json"}


def fetch_airport_data(list_airports, limit=1000):
    TOKEN = config["keys"]["TOKEN_AIRPORT"]
    URL = gv.URL_AIRPORT+"access_key="+TOKEN
    all_rows = []
    offset = 0

    while True:
        params = {
            "access_key": TOKEN,
            "limit": limit,
            "offset": offset,
        }
        response = requests.get(URL, headers=headers,
                                params=params, timeout=15)

        if response.status_code != 200:
            print("Error:", response.text)
            break

        body = response.json()
        data = body.get("data", [])
        pagination = body.get("pagination", {})
        count = pagination.get("count", len(data))
        total = pagination.get("total")
        if not data:
            break

        all_rows.extend(data)
        offset += count
        if total is not None and offset >= total:
            break
    result = {}
    for index, row in enumerate(all_rows):
        if not row.get("icao_code"):
            continue
        if row.get("icao_code") not in list_airports:
            continue

        result[row.get("icao_code")] = {
            "id": index,
            "longitude": row.get("longitude"),
            "latitude": row.get("latitude"),
            "name": row.get("airport_name"),
            "city": row.get("city_iata_code"),
            "country": row.get("country_name"),
        }

    with open(gv.AIRPORT_LOCATION_PATH, mode="w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


def _fetch_one_species(species_name):
    try:
        resp = requests.get(
            gv.URL_SPECIES,
            headers=headers,
            params={"q": species_name},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])

        if not results:
            print(f"No species found for '{species_name}'")
            return []

        rows = []
        for r in results:
            rows.append({
                "input_name": species_name,
                "usageKey": r.get("usageKey", ""),
                "scientificName": r.get("scientificName", ""),
                "canonicalName": r.get("canonicalName", ""),
                "rank": r.get("rank", ""),
                "kingdom": r.get("kingdom", ""),
                "phylum": r.get("phylum", ""),
                "class": r.get("class", ""),
                "order": r.get("order", ""),
                "family": r.get("family", ""),
                "genus": r.get("genus", ""),
                "species": r.get("species", ""),
                "taxonomicStatus": r.get("taxonomicStatus", "")
            })
        return rows

    except requests.RequestException as e:
        print(f"Error fetching {species_name}: {e}")
        return []


def fetch_species_data(list_species_name, max_workers=50):
    all_rows = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        async_jobs_list = {
            executor.submit(_fetch_one_species, species): species
            for species in list_species_name
        }

        for async_job in as_completed(async_jobs_list):
            species_name = async_jobs_list[async_job]
            try:
                rows = async_job.result()
                all_rows.extend(rows)
            except Exception as e:
                print(f"Error for {species_name} {e}")

    with open(gv.SPECIES_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    print(f"Saved species details to {gv.SPECIES_PATH}")


if __name__ == "__main__":
    airport_list = set()
    species_list = set()
    isheader = True
    for batch in batch_reader(gv.CLEANED_DATABASE_PATH, batch_size=8000):
        for line in batch:
            if isheader:
                isheader = False
                continue
            row = next(csv.reader([line]))
            species_name = row[31].strip()
            if species_name and species_name.upper() not in ('', "UNK", "UNKNOWN"):
                species_list.add(species_name)
            icao_code = row[19].strip()
            if icao_code and re.fullmatch(r'[A-Za-z]{4}', icao_code):
                airport_list.add(icao_code)
    fetch_airport_data(list(airport_list))
    fetch_species_data(list(species_list))
