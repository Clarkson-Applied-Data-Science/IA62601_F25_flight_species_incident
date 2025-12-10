# Species & Aviation Data Loader

The starting point of this work was a csv file that contains the strike that happened between 1990 - 1992. The data contains 66 columns and 174104 raw rows.

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
| 1 | BUDGERIGAR | Papovaviricetes | 1 |
| 2 | EVENING GROSBEAK | Aves | 1 |
| 3 | BADGER | Pisoniviricetes | 1 |
| 4 | POCKETED FREE-TAILED BAT | Mammalia | 1 |
| 5 | RED-NECKED GREBE | Insthoviricetes | 1 |
| 6 | EASTERN DIAMONDBACK RATTLESNAKE |  | 1 |
| 7 | TUFTED TITMOUSE | Aves | 1 |
| 8 | HELMETED GUINEAFOWL | Aves | 1 |
| 9 | RUSTY BLACKBIRD | Aves | 1 |
| 10 | SOOTY TERN | Aves | 1 |

---

**1.2 Class-level patterns**  
_Which taxonomic class (e.g., birds vs. mammals vs. other) is most commonly involved in incidents?_

Incident counts by class:

| Class | Incidents |
| --- | --- |
|  | 33314 |
| Aves | 27492 |
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
| 6 | MOURNING DOVE | Aves | 342 |
| 7 | CANADA GOOSE | Insthoviricetes | 342 |
| 8 | HAWK | Insthoviricetes | 327 |
| 9 | KILLDEER | Aves | 296 |
| 10 | EUROPEAN STARLING | Aves | 284 |

---

#### 2. By Airport / Airline

**2.1 Airport risk**  
_Which airports have the highest number of wildlife incidents?_

Top 10 airports by incident count:

| Rank | Airport | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | DALLAS/FORT WORTH INTL ARPT | KDFW | 2144 |
| 2 | DENVER INTL AIRPORT | KDEN | 1950 |
| 3 | SACRAMENTO INTL | KSMF | 1630 |
| 4 | CHICAGO O'HARE INTL ARPT | KORD | 1554 |
| 5 | PHILADELPHIA INTL | KPHL | 1276 |
| 6 | ORLANDO INTL | KMCO | 1249 |
| 7 | JOHN F KENNEDY INTL | KJFK | 1237 |
| 8 | MEMPHIS INTL | KMEM | 1200 |
| 9 | LA GUARDIA ARPT | KLGA | 1182 |
| 10 | SALT LAKE CITY INTL | KSLC | 1179 |

---

**2.2 Airline risk**  
_Which airlines have the most incidents?_

Top 10 airlines by incident count:

| Rank | Airline | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | BUSINESS | BUS | 10220 |
| 2 | SOUTHWEST AIRLINES | SWA | 9626 |
| 3 | AMERICAN AIRLINES | AAL | 7164 |
| 4 | DELTA AIR LINES | DAL | 4284 |
| 5 | UNITED AIRLINES | UAL | 3712 |
| 6 | MILITARY | MIL | 3463 |
| 7 | FEDEX EXPRESS | FDX | 2877 |
| 8 | 1US AIRWAYS | USA | 2776 |
| 9 | SKYWEST AIRLINES | SKW | 2348 |
| 10 | AMERICAN EAGLE AIRLINES | EGF | 2169 |

---

#### 3. Temporal Patterns

**3.1 Trends over time**  
_How have incident counts changed by year?_

Incident counts by year:

| Year | Incidents |
| --- | --- |
| 2014 | 7215 |
| 2012 | 5717 |
| 2013 | 5580 |
| 2011 | 5171 |
| 2015 | 4921 |
| 2010 | 4905 |
| 2009 | 4279 |
| 2007 | 3271 |
| 2008 | 3190 |
| 2006 | 3107 |
| 2004 | 2886 |
| 2005 | 2833 |
| 2002 | 2624 |
| 2003 | 2596 |
| 2000 | 2396 |
| 2001 | 2393 |
| 1999 | 1902 |
| 1998 | 1878 |
| 1997 | 1659 |
| 1994 | 1603 |
| 1995 | 1568 |
| 1996 | 1511 |
| 1993 | 1510 |
| 1992 | 1489 |
| 1991 | 1433 |
| 1990 | 1192 |

---

**3.2 Seasonality**  
_Are incidents more common in certain months or seasons?_

By month:

| Month # | Month | Incidents |
| --- | --- | --- |
| 8 | August | 11653 |
| 9 | September | 10564 |
| 7 | July | 10274 |
| 10 | October | 8882 |
| 5 | May | 7624 |
| 6 | June | 6588 |
| 4 | April | 5606 |
| 11 | November | 5247 |
| 3 | March | 3782 |
| 12 | December | 3239 |
| 1 | January | 2838 |
| 2 | February | 2532 |

Based on the incident data, wildlife strikes peak in **May** and **September**.  
This pattern is consistent with independent migration data which I found on :

- eBird Status & Trends and BirdCast show the highest migration intensity during late spring (May) and early fall across much of North America.
- USGS waterbird migration studies define spring migration as April–May and fall migration as August–October, bracketing the May and September peaks seen in our dataset.

Although this might feel over generalization since exact timing varies by species and latitude these external data sources support that our “migration" might be causing higher incident in these months.
