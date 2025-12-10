# Species & Aviation Data Loader

This project contains a set of Python scripts to batch-load CSV data into a MySQL database.  
It currently supports:

- Species → `species` table
- Airlines → `airline` table
- Airports → `airport` table
- Flights → `flight` table
- Incidents → `incident` table

## Questions & Analyses

### Dynamic summaries

#### 1. By Species / Taxonomic Class

**1.1 Species-level frequency**  
_Which species are involved in the highest number of incidents?_

Top 10 species by incident count:

| Rank | Species | Taxonomic Class | Incidents |
| --- | --- | --- | --- |
| 1 | UNKNOWN SMALL BIRD |  | 887 |
| 2 | GULL | Arfiviricetes | 689 |
| 3 | SPARROW | Chytridiomycetes | 170 |
| 4 | BLACKBIRD | Repensiviricetes | 144 |
| 5 | ROCK PIGEON | Aves | 113 |
| 6 | EUROPEAN STARLING | Aves | 95 |
| 7 | CANADA GOOSE | Insthoviricetes | 83 |
| 8 | WHITE-TAILED DEER | Mammalia | 74 |
| 9 | DUCK | Aves | 71 |
| 10 | HAWK | Insthoviricetes | 68 |

---

_Which species are involved in the low number of incidents?_

Bottom 10 species by incident count:

| Rank | Species | Taxonomic Class | Incidents |
| --- | --- | --- | --- |
| 1 | SAVANNAH SPARROW | Aves | 1 |
| 2 | EASTERN SCREECH-OWL | Aves | 1 |
| 3 | DOMESTIC CAT | Mammalia | 1 |
| 4 | OLD WORLD VULTURES |  | 1 |
| 5 | NORTHERN MOCKINGBIRD | Aves | 1 |
| 6 | GREEN-WINGED TEAL | Insthoviricetes | 1 |
| 7 | YELLOW-BILLED CUCKOO | Aves | 1 |
| 8 | WOODCHUCK | Revtraviricetes | 1 |
| 9 | EASTERN KINGBIRD | Aves | 1 |
| 10 | FOXES | Mammalia | 1 |

---

**1.2 Class-level patterns**  
_Which taxonomic class (e.g., birds vs. mammals vs. other) is most commonly involved in incidents?_

Incident counts by class:

| Class | Incidents |
| --- | --- |
|  | 937 |
| Aves | 803 |
| Arfiviricetes | 689 |
| Insthoviricetes | 228 |
| Chytridiomycetes | 170 |
| Repensiviricetes | 144 |
| Mammalia | 80 |
| Trematoda | 41 |
| Gastropoda | 23 |
| Cyanophyceae | 12 |

---

**1.3 Species–airport spread**  
_For each species, at how many different airports has it been recorded in incidents?_

Top 10 species by number of affected airports:

| Rank | Species | Class | # Airports |
| --- | --- | --- | --- |
| 1 | UNKNOWN SMALL BIRD |  | 211 |
| 2 | GULL | Arfiviricetes | 186 |
| 3 | SPARROW | Chytridiomycetes | 98 |
| 4 | BLACKBIRD | Repensiviricetes | 85 |
| 5 | WHITE-TAILED DEER | Mammalia | 58 |
| 6 | EUROPEAN STARLING | Aves | 58 |
| 7 | ROCK PIGEON | Aves | 58 |
| 8 | DUCK | Aves | 55 |
| 9 | CANADA GOOSE | Insthoviricetes | 52 |
| 10 | HAWK | Insthoviricetes | 49 |

---

#### 2. By Airport / Airline

**2.1 Airport risk**  
_Which airports have the highest number of wildlife incidents?_

Top 10 airports by incident count:

| Rank | Airport | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | DALLAS/FORT WORTH INTL ARPT | KDFW | 138 |
| 2 | NASHVILLE INTL | KBNA | 81 |
| 3 | CHICAGO O'HARE INTL ARPT | KORD | 65 |
| 4 | JOHN F KENNEDY INTL | KJFK | 60 |
| 5 | LA GUARDIA ARPT | KLGA | 60 |
| 6 | NORFOLK INTL | KORF | 57 |
| 7 | PHILADELPHIA INTL | KPHL | 47 |
| 8 | SAN FRANCISCO INTL ARPT | KSFO | 47 |
| 9 | PITTSBURGH INTL ARPT | KPIT | 44 |
| 10 | MIAMI INTL | KMIA | 43 |

---

**2.2 Airline risk**  
_Which airlines have the most incidents?_

Top 10 airlines by incident count:

| Rank | Airline | ICAO | Incidents |
| --- | --- | --- | --- |
| 1 | AMERICAN AIRLINES | AAL | 811 |
| 2 | BUSINESS | BUS | 468 |
| 3 | 1US AIRWAYS | USA | 341 |
| 4 | SOUTHWEST AIRLINES | SWA | 154 |
| 5 | MILITARY | MIL | 149 |
| 6 | PRIVATELY OWNED | PVT | 147 |
| 7 | UNITED AIRLINES | UAL | 117 |
| 8 | DELTA AIR LINES | DAL | 91 |
| 9 | NORTHWEST AIRLINES | NWA | 91 |
| 10 | CONTINENTAL AIRLINES | COA | 68 |

---

#### 3. Temporal Patterns

**3.1 Trends over time**  
_How have incident counts changed by year?_

Incident counts by year:

| Year | Incidents |
| --- | --- |
| 1990 | 1192 |
| 1991 | 1433 |
| 1992 | 531 |

---

**3.2 Seasonality**  
_Are incidents more common in certain months or seasons?_

By month:

| Month # | Month | Incidents |
| --- | --- | --- |
| 5 | May | 401 |
| 9 | September | 372 |
| 8 | August | 346 |
| 10 | October | 333 |
| 7 | July | 324 |
| 6 | June | 315 |
| 11 | November | 255 |
| 4 | April | 225 |
| 3 | March | 181 |
| 12 | December | 136 |
| 1 | January | 136 |
| 2 | February | 132 |
