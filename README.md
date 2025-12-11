# Species & Aviation Data Loader

The starting point of this work was a csv file downloaded from https://www.kaggle.com/datasets/faa/wildlife-strikes that contains the strike that happened between 1990 - 2015. The data contains 66 columns and 174104 raw rows.

Here is a description about the columns https://wildlife.faa.gov/assets/fieldlist.pdf
| Dtype | Columns |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| int64 | Record ID, Incident Year, Incident Month, Incident Day, Aircraft Damage, Radome Strike, Radome Damage, Windshield Strike, Windshield Damage, Nose Strike, Nose Damage, Engine1 Strike, Engine1 Damage, Engine2 Strike, Engine2 Damage, Engine3 Strike, Engine3 Damage, Engine4 Strike, Engine4 Damage, Engine Ingested, Propeller Strike, Propeller Damage, Wing or Rotor Strike, Wing or Rotor Damage, Fuselage Strike, Fuselage Damage, Landing Gear Strike, Landing Gear Damage, Tail Strike, Tail Damage, Lights Strike, Lights Damage, Other Strike, Other Damage |
| float64 | Aircraft Mass, Engine Make, Engines, Engine2 Position, Engine4 Position, Height, Speed, Distance, Fatalities, Injuries |
| object | Operator ID, Operator, Aircraft, Aircraft Type, Aircraft Make, Aircraft Model, Engine Model, Engine Type, Engine1 Position, Engine3 Position, Airport ID, Airport, State, FAA Region, Warning Issued, Flight Phase, Visibility, Precipitation, Species ID, Species Name, Species Quantity, Flight Impact |

The data was the base point from this I wanted to acheive the points below

- 1 Create a bucket by taking the species name and decrease the types

  I researched for sites that can get me the rank,kingdom,phylum,class based on species name. Most sites I found were paid for and since I had 773 species that was not an option. I then found GBIF (the Global Biodiversity Information Facility). It is an international network and data infrastructure funded by the world's governments and aimed at providing anyone, anywhere, open access to data about all types of life on Earth. I used https://api.gbif.org/v1/species/search end point. The end point takes one species at a time so I had to create 20 Threads to shorten the fetching time and went through the 773 species. The return data per species is a list of entries with these keys input_name,usageKey,scientificName,canonicalName,rank,kingdom,phylum,class,order,family,genus,species,taxonomicStatus. Since one species has many class names I had to find a way to do 1to1 mapping. After this I created a function to count the species and the classes and then take the class with the highest count and then populate mySQL table accordingly.

- 2 Using the airport icao fetch information about the location of the airport

  There are many companies that offers airport information details. But almost all had some fee attached to them. I used https://api.aviationstack.com/v1/airports. I was able to get the id,gmt,airport_id,iata_code,city_iata_code,icao_code,country_iso2,geoname_id,latitude,longitude,airport_name,country_name,phone_number,timezone.

- 3 Create a migration information and map that to the flights

  Although I have attempted this I was faced with many blockers starting from how the data was first shaped. The incident location is not in the data hence there is no way I can relate the path of the species migration to the incident location. Instead what I did was use Cornell Lab of Ornithology (https://api.ebird.org/v2/data/obs/KZ/recent) to study the migration of birds and see if the seasonality information I get from the data analysis I did in the end truly aligns which did.

After collecting all data locally, I processed it in batches due to its size. For each batch, I first populated the dimension tables, retrieved the generated IDs, and then populated the fact table with those IDs and the remaining attributes.

Using this schema, I implemented a series of queries to answer the analytical questions described below. Because the dataset continues to evolve as additional EDA and cleaning are performed, I added a README generator script: whenever the data processing changes, you can re-run the generator to automatically refresh the dynamic summaries in the README.

Before running the project, copy config.example.yml to config.yml and update it with your database connection details and table names.

## Database diagram

I have added the foreign key for depiction but you can remove them to make it easier.
![Diagram](db_diagram.png)

Steps to start

- 1 Download the raw data from https://www.kaggle.com/datasets/faa/wildlife-strikes put it under data folder or go and edit the global_vars to match your structre
- 2 There is SQL dump of the table structure you can import that to Mysql then run the data
- 3 Edit your config file use the names that you gave to your tables
- 4 Run the data_fetcher.py
- 5 Run main.py to populate table
- 6 Run generate_readme.py to see a textual explanation or run question_answer to see the answers

## Questions & Analyses

#### 1. By Species / Taxonomic Class

**1.1 Species-level frequency**  
_Which species are involved in the highest number of incidents?_

Top 10 species by incident count:

| Rank | Species | Taxonomic Class | Incidents |
| --- | --- | --- | --- |
| 1 | UNKNOWN SMALL BIRD |  | 27734 |
| 2 | GULL | Arfiviricetes | 5381 |
| 3 | UNKNOWN BIRD |  | 4524 |
| 4 | MOURNING DOVE | Aves | 2787 |
| 5 | SPARROW | Chytridiomycetes | 2257 |
| 6 | EUROPEAN STARLING | Aves | 2249 |
| 7 | BARN SWALLOW | Aves | 2065 |
| 8 | ROCK PIGEON | Aves | 1625 |
| 9 | HORNED LARK | Aves | 1446 |
| 10 | KILLDEER | Aves | 1428 |

---

_Which species are involved in the low number of incidents?_

Bottom 10 species by incident count:

| Rank | Species | Taxonomic Class | Incidents |
| --- | --- | --- | --- |
| 1 | WHITE-BELLIED SEA-EAGLE | Aves | 1 |
| 2 | CATS | Mammalia | 1 |
| 3 | WHITE-TAILED PRAIRIE DOG | Mammalia | 1 |
| 4 | HUDSONIAN GODWIT | Aves | 1 |
| 5 | BUDGERIGAR | Papovaviricetes | 1 |
| 6 | NORTHERN FULMAR | Aves | 1 |
| 7 | WHITE STORK | Aves | 1 |
| 8 | PIPING PLOVER | Aves | 1 |
| 9 | BLACK-THROATED GRAY WARBLER | Aves | 1 |
| 10 | BRANDT'S CORMORANT | Aves | 1 |

---

**1.2 Class-level patterns**  
_Which taxonomic class (e.g., birds vs. mammals vs. other) is most commonly involved in incidents?_

Incident counts by class:

| Class | Incidents |
| --- | --- |
|  | 33318 |
| Aves | 27676 |
| Insthoviricetes | 5482 |
| Arfiviricetes | 5382 |
| Chytridiomycetes | 2257 |
| Mammalia | 1382 |
| Repensiviricetes | 1122 |
| Gastropoda | 781 |
| Trematoda | 652 |
| Insecta | 351 |

---

**1.3 Species–airport spread**  
_For each species, at how many different airports has it been recorded in incidents?_

Top 10 species by number of affected airports:

| Rank | Species | Class | # Airports |
| --- | --- | --- | --- |
| 1 | UNKNOWN SMALL BIRD |  | 1019 |
| 2 | GULL | Arfiviricetes | 568 |
| 3 | UNKNOWN BIRD |  | 484 |
| 4 | SPARROW | Chytridiomycetes | 399 |
| 5 | WHITE-TAILED DEER | Mammalia | 374 |
| 6 | CANADA GOOSE | Insthoviricetes | 342 |
| 7 | MOURNING DOVE | Aves | 342 |
| 8 | HAWK | Insthoviricetes | 327 |
| 9 | KILLDEER | Aves | 296 |
| 10 | EUROPEAN STARLING | Aves | 284 |

---

_Are high-risk airports close together or spread out?_

For each high-risk airport, I identified top 5 airports and their 2 nearest high-risk neighbors and computed the great-circle distance between them using haversine.
The table below shows example airport pairs, their incident counts, and how far apart they are. This function can 
be extended to all high-risk airports to analyze spatial clustering for the further study.

| Rank | Airport pair (origin → neighbor) | Incidents (origin / neighbor) | Distance (mile) |
| --- | --- | --- | --- |
| 1 | DALLAS/FORT WORTH INTL ARPT → DENVER INTL AIRPORT | 2150 / 1951 | 640.7 |
| 2 | DALLAS/FORT WORTH INTL ARPT → CHICAGO O'HARE INTL ARPT | 2150 / 1565 | 801.8 |
| 3 | DALLAS/FORT WORTH INTL ARPT → PHILADELPHIA INTL | 2150 / 1283 | 1300.3 |
| 4 | DENVER INTL AIRPORT → DALLAS/FORT WORTH INTL ARPT | 1951 / 2150 | 640.7 |
| 5 | DENVER INTL AIRPORT → CHICAGO O'HARE INTL ARPT | 1951 / 1565 | 886.3 |
| 6 | DENVER INTL AIRPORT → SACRAMENTO INTL | 1951 / 1643 | 907.3 |
| 7 | SACRAMENTO INTL → DENVER INTL AIRPORT | 1643 / 1951 | 907.3 |
| 8 | SACRAMENTO INTL → DALLAS/FORT WORTH INTL ARPT | 1643 / 2150 | 1428.4 |
| 9 | SACRAMENTO INTL → CHICAGO O'HARE INTL ARPT | 1643 / 1565 | 1777.2 |
| 10 | CHICAGO O'HARE INTL ARPT → PHILADELPHIA INTL | 1565 / 1283 | 676.0 |
| 11 | CHICAGO O'HARE INTL ARPT → DALLAS/FORT WORTH INTL ARPT | 1565 / 2150 | 801.8 |
| 12 | CHICAGO O'HARE INTL ARPT → DENVER INTL AIRPORT | 1565 / 1951 | 886.3 |
| 13 | PHILADELPHIA INTL → CHICAGO O'HARE INTL ARPT | 1283 / 1565 | 676.0 |
| 14 | PHILADELPHIA INTL → DALLAS/FORT WORTH INTL ARPT | 1283 / 2150 | 1300.3 |
| 15 | PHILADELPHIA INTL → DENVER INTL AIRPORT | 1283 / 1951 | 1553.7 |

---

#### 2. By Airport / Airline

**2.1 Airport risk**  
_Which airports have the highest number of wildlife incidents?_

Top 10 airports by incident count:

| Rank | Airport | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | DALLAS/FORT WORTH INTL ARPT | KDFW | 2150 |
| 2 | DENVER INTL AIRPORT | KDEN | 1951 |
| 3 | SACRAMENTO INTL | KSMF | 1643 |
| 4 | CHICAGO O'HARE INTL ARPT | KORD | 1565 |
| 5 | PHILADELPHIA INTL | KPHL | 1283 |
| 6 | ORLANDO INTL | KMCO | 1249 |
| 7 | JOHN F KENNEDY INTL | KJFK | 1239 |
| 8 | MEMPHIS INTL | KMEM | 1203 |
| 9 | LA GUARDIA ARPT | KLGA | 1184 |
| 10 | SALT LAKE CITY INTL | KSLC | 1183 |

---

**2.2 Airline risk**  
_Which airlines have the most incidents?_

Top 10 airlines by incident count:

| Rank | Airline | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | BUSINESS | BUS | 10240 |
| 2 | SOUTHWEST AIRLINES | SWA | 9647 |
| 3 | AMERICAN AIRLINES | AAL | 7174 |
| 4 | DELTA AIR LINES | DAL | 4293 |
| 5 | UNITED AIRLINES | UAL | 3721 |
| 6 | MILITARY | MIL | 3510 |
| 7 | FEDEX EXPRESS | FDX | 2885 |
| 8 | 1US AIRWAYS | USA | 2782 |
| 9 | SKYWEST AIRLINES | SKW | 2349 |
| 10 | AMERICAN EAGLE AIRLINES | EGF | 2171 |

---

#### 3. Temporal Patterns

**3.1 Trends over time**  
_How have incident counts changed by year?_

Incident counts by year:

| Year | Incidents |
| --- | --- |
| 2014 | 7219 |
| 2012 | 5726 |
| 2013 | 5585 |
| 2011 | 5178 |
| 2015 | 4924 |
| 2010 | 4909 |
| 2009 | 4281 |
| 2007 | 3275 |
| 2008 | 3191 |
| 2006 | 3115 |
| 2004 | 2898 |
| 2005 | 2840 |
| 2002 | 2631 |
| 2003 | 2603 |
| 2000 | 2403 |
| 2001 | 2401 |
| 1999 | 1914 |
| 1998 | 1890 |
| 1997 | 1669 |
| 1994 | 1619 |
| 1995 | 1576 |
| 1993 | 1521 |
| 1996 | 1521 |
| 1992 | 1497 |
| 1991 | 1437 |
| 1990 | 1197 |

---

**3.2 Seasonality**  
_Are incidents more common in certain months or seasons?_

By month:

| Month # | Month | Incidents |
| --- | --- | --- |
| 8 | August | 11671 |
| 9 | September | 10580 |
| 7 | July | 10286 |
| 10 | October | 8907 |
| 5 | May | 7632 |
| 6 | June | 6593 |
| 4 | April | 5622 |
| 11 | November | 5272 |
| 3 | March | 3801 |
| 12 | December | 3258 |
| 1 | January | 2853 |
| 2 | February | 2545 |

Based on the incident data, wildlife strikes peak in fall and late spring.  
This pattern is consistent with independent migration information which I found on :

- eBird Status & Trends and BirdCast show the highest migration intensity during late spring (May) and early fall across much of North America.
- USGS waterbird migration studies define spring migration as April–May and fall migration as August–October, bracketing the May and September peaks seen in our dataset.

Although this might feel over generalization since exact timing varies by species and latitude these external data sources support that our “migration" might be causing higher incident in these months.
