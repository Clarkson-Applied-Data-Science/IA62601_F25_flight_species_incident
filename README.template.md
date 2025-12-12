# Species & Aviation Data Loader

The starting point of this work was a csv file downloaded from https://www.kaggle.com/datasets/faa/wildlife-strikes that contains the strike that happened between 1990 - 2015. The data contains 66 columns and 174104 raw rows.

Here is a description about the columns https://wildlife.faa.gov/assets/fieldlist.pdf
| Dtype | Columns |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| int64 | Record ID, Incident Year, Incident Month, Incident Day, Aircraft Damage, Radome Strike, Radome Damage, Windshield Strike, Windshield Damage, Nose Strike, Nose Damage, Engine1 Strike, Engine1 Damage, Engine2 Strike, Engine2 Damage, Engine3 Strike, Engine3 Damage, Engine4 Strike, Engine4 Damage, Engine Ingested, Propeller Strike, Propeller Damage, Wing or Rotor Strike, Wing or Rotor Damage, Fuselage Strike, Fuselage Damage, Landing Gear Strike, Landing Gear Damage, Tail Strike, Tail Damage, Lights Strike, Lights Damage, Other Strike, Other Damage |
| float64 | Aircraft Mass, Engine Make, Engines, Engine2 Position, Engine4 Position, Height, Speed, Distance, Fatalities, Injuries |
| object | Operator ID, Operator, Aircraft, Aircraft Type, Aircraft Make, Aircraft Model, Engine Model, Engine Type, Engine1 Position, Engine3 Position, Airport ID, Airport, State, FAA Region, Warning Issued, Flight Phase, Visibility, Precipitation, Species ID, Species Name, Species Quantity, Flight Impact |

The data was the base point from this I wanted to acheive the points below

## Objective

1. Create a bucket by taking the species name and decrease the types

   I researched for sites that can get me the rank,kingdom,phylum,class based on species name. Most sites I found were paid for and since I had 773 species that was not an option. I then found GBIF (the Global Biodiversity Information Facility). It is an international network and data infrastructure funded by the world's governments and aimed at providing anyone, anywhere, open access to data about all types of life on Earth. I used https://api.gbif.org/v1/species/search end point. The end point takes one species at a time so I had to create 20 Threads to shorten the fetching time and went through the 773 species. The return data per species is a list of entries with these keys input_name,usageKey,scientificName,canonicalName,rank,kingdom,phylum,class,order,family,genus,species,taxonomicStatus. Since one species has many class names I had to find a way to do 1to1 mapping. After this I created a function to count the species and the classes and then take the class with the highest count and then populate mySQL table accordingly.

2. Using the airport icao fetch information about the location of the airport

   There are many companies that offers airport information details. But almost all had some fee attached to them. I used https://api.aviationstack.com/v1/airports. I was able to get the id,gmt,airport_id,iata_code,city_iata_code,icao_code,country_iso2,geoname_id,latitude,longitude,airport_name,country_name,phone_number,timezone.

3. Answer the analytical question and see if there is a seasonality in these data.

   Based on the incident data, wildlife strikes peak in fall and late spring.  
   This pattern is consistent with independent migration information which I found on :

   - eBird Status & Trends and BirdCast show the highest migration intensity during late spring (May) and early fall across much of North America.
   - USGS waterbird migration studies define spring migration as April–May and fall migration as August–October, bracketing the May and September peaks seen in our dataset.

   Although this might feel over generalization since exact timing varies by species and latitude these external data sources support that our “migration" might be causing higher incident in these months.

4. Create a migration information and map that to the flights

   Although I have attempted this I was faced with many blockers starting from how the data was first shaped. The incident location is not in the data hence there is no way I can relate the path of the species migration to the incident location. Instead what I did was use Cornell Lab of Ornithology (https://api.ebird.org/v2/data/obs/KZ/recent) to study the migration of birds and see if the seasonality information I get from the data analysis I did in the end truly aligns which did.

## ETL

- After collecting the raw data locally using the `data_fetched.py` (Extract) via avaliable API mentioned above, I processed the incident data in batches(5000) due to its size. For each batch, I first cleaned and reshaped the data into a star-schema structure (Transform), then populated the dimension tables, retrieved the generated IDs, and loaded the fact table(the incident) with those IDs and the remaining attributes (Load).

- Using this schema, I implemented a series of queries to answer the analytical questions described below. Because the dataset continues to evolve as additional EDA and cleaning are performed, I added a README generator script: whenever the data processing changes, you can re-run the generator to automatically refresh the dynamic summaries in the README.

- Before running the project, copy `config.example.yml` to `config.yml` and update it with your database connection details and table names.

## Database diagram

I have added the foreign key for depiction but you can remove them to make it easier.

![Diagram](db_diagram.png)

# Steps to start

- 1 Download the raw data from https://www.kaggle.com/datasets/faa/wildlife-strikes put it under data folder or go and edit the global_vars to match your structre
- 2 There is SQL dump of the table structure you can import that to Mysql then run the data
- 3 Edit your config file use the names that you gave to your tables
- 4 Run the data_fetcher.py
- 5 Run main.py to populate table. If you are checking my DB then you have to use the gurmesea_airline_strike DB
- 6 Run generate_readme.py to see a textual explanation or run question_answer to see the answers

## Questions & Analyses
