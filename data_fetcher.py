import requests
import pandas as pd
import csv  
from concurrent.futures import ThreadPoolExecutor, as_completed
import global_vars as gv

FIELDNAMES = [
    "input_name", "usageKey", "scientificName", "canonicalName",
    "rank", "kingdom", "phylum", "class", "order", "family",
    "genus", "species", "taxonomicStatus"
]
headers = {"Accept": "application/json"}
def fetch_airport_data(list_airports=[]): 
    TOKEN = "218666285bd4894309ab922ef8bff157"  
    URL = gv.URL_AIRPORT + TOKEN
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", [])
        df = pd.DataFrame(data)
        df.to_csv(gv.AIRPORT_LOCATION_PATH, index=False)
        print("Saved to tempo.csv")
    else:
        print("Error:", response.text)

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


def fetch_species_data(list_species_name, max_workers=20):
    all_rows = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {
            executor.submit(_fetch_one_species, sp): sp
            for sp in list_species_name
        }

        for future in as_completed(future_to_name):
            species_name = future_to_name[future]
            try:
                rows = future.result()
                all_rows.extend(rows)
            except Exception as e:
                print(f"Unexpected error for {species_name}: {e}")

    with open(gv.SPECIES_PATH, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    print(f"Saved species details to {gv.SPECIES_PATH}")
