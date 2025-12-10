# Species & Aviation Data Loader

This project contains a set of Python scripts to batch-load CSV data into a MySQL database.  
It currently supports:

- Species → `species` table  
- Airlines → `airline` table  
- Airports → `airport` table  
- Flights → `flight` table  
- Incidents → `incident` table  

The code reads large CSV files in batches, deduplicates some entries in memory, and writes them into the configured database tables.

# Project structure
.
├── config.yml
├── global_vars.py
├── data_fetcher.py
├── loader.py          # (this script)
└── data/
    ├── species.csv    # path used by gv.SPECIES_PATH
    └── raw_db.csv     # path used by gv.RAW_DATABASE_PATH
    ├── airport_location.csv    # path used by gv.AIRPORT_LOCATION_PATH
    └── ambiguous_species.csv     # path used by gv.AMBIGUOUS_SPECIES_PATH

https://science.ebird.org/en/status-and-trends/species/budger/abundance-map

## Questions & Analyses

This dataset supports a wide range of ecological and aviation-safety questions. 
Altitude related analysis , 
### 1. By Species / Taxonomic Class

- **Species-level frequency**
  - Which species are involved in the highest number of incidents?
- **Class-level patterns**
  - Which taxonomic class (e.g., birds vs. mammals vs. other) is most commonly involved in incidents?
- **Species–airport spread**
  - For each species, at how many different airports has it been recorded in incidents?

### 2. By Airport / Airline

- **Airport risk**
  - Which airports have the highest number of wildlife incidents?
- **Airline risk and exposure**
  - Which airlines have the most incidents?
  - Are those counts explained simply by higher traffic volume, or do some airlines have higher incident *rates* per flight?

### 3. Temporal Patterns

- **Trends over time**
  - How have incident counts changed by year?
- **Seasonality**
  - Are incidents more common in certain months or seasons?

### 4. Species Behavior & Ecology

- **Migratory species**
  - Are migratory birds involved in more incidents during known migration months?
- **Body size and severity**
  - Do large-bodied species (e.g., geese, deer) correlate with more severe damage than small-bodied species (e.g., small passerines)?

### 5. Airport Differences

- **Coastal vs. inland**
  - Do coastal airports vs. inland airports show different species profiles in wildlife incidents?
- **Regional patterns**
  - Are airports in certain countries or regions more affected by particular taxonomic classes (e.g., waterfowl vs. raptors)?



 
