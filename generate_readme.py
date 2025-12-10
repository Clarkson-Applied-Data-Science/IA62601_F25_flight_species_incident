from pathlib import Path
from textwrap import dedent
import global_vars as gv
from question_answer import (
    q_1_species_level_frequency,
    q_1b_species_level_frequency,
    q_2_class_level_patterns,
    q_3_species_airport_spread,
    q_4_airport_risk,
    q_5_airline_incident_counts,
    q_6_trends_over_time_by_year,
    q_7_incidents_by_month
)


def md_table(rows, headers):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def markdown():
    sections = []

    species = q_1_species_level_frequency(top_n=10)
    species_rows = [(i + 1, row["species_name"], row["taxonomic_class"],
                     row["incident_count"]) for i, row in enumerate(species)]
    sections.append(dedent(f"""
### Dynamic summaries

#### 1. By Species / Taxonomic Class

**1.1 Species-level frequency**  
_Which species are involved in the highest number of incidents?_

Top 10 species by incident count:

{md_table(species_rows, ["Rank", "Species", "Taxonomic Class", "Incidents"])}
""").strip())
    species = q_1b_species_level_frequency(low_n=10)
    species_rows = [(i + 1, row["species_name"], row["taxonomic_class"],
                    row["incident_count"]) for i, row in enumerate(species)]
    sections.append(dedent(f"""
_Which species are involved in the low number of incidents?_

Bottom 10 species by incident count:

{md_table(species_rows, ["Rank", "Species", "Taxonomic Class", "Incidents"])}
""").strip())

    classes = q_2_class_level_patterns()
    class_rows = [(row["taxonomic_class"], row["incident_count"])
                  for row in classes]
    sections.append(dedent(f"""
**1.2 Class-level patterns**  
_Which taxonomic class (e.g., birds vs. mammals vs. other) is most commonly involved in incidents?_

Incident counts by class:

{md_table(class_rows, ["Class", "Incidents"])}""").strip())

    species_airports = q_3_species_airport_spread(top_n=10)
    species_airport_rows = [
        (i + 1, row["species_name"], row["class"], row["airport_count"])
        for i, row in enumerate(species_airports)
    ]
    sections.append(dedent(f"""
**1.3 Species–airport spread**  
_For each species, at how many different airports has it been recorded in incidents?_

Top 10 species by number of affected airports:

{md_table(species_airport_rows, ["Rank", "Species", "Class", "# Airports"])}
            """).strip())

    airports = q_4_airport_risk(top_n=10)
    airport_rows = [
        (i + 1, row["airport_name"], row["icao"], row["incident_count"])
        for i, row in enumerate(airports)
    ]
    sections.append(dedent(f"""
#### 2. By Airport / Airline

**2.1 Airport risk**  
_Which airports have the highest number of wildlife incidents?_

Top 10 airports by incident count:

{md_table(airport_rows, ["Rank", "Airport", "ICAO", "Incidents"])}
            """).strip())

    airlines = q_5_airline_incident_counts(top_n=10)
    airline_rows = [(i + 1, row["airline"], row["icao"],
                     row["incident_count"]) for i, row in enumerate(airlines)]
    sections.append(dedent(f"""
**2.2 Airline risk**  
_Which airlines have the most incidents?_

Top 10 airlines by incident count:

{md_table(airline_rows, ["Rank", "Airline", "ICAO", "Incidents"])}
            """).strip())

    yearly = q_6_trends_over_time_by_year()
    year_rows = [(row["year"], row["incident_count"]) for row in yearly]
    sections.append(dedent(f"""
#### 3. Temporal Patterns

**3.1 Trends over time**  
_How have incident counts changed by year?_

Incident counts by year:

{md_table(year_rows, ["Year", "Incidents"])}
            """).strip())

    monthly = q_7_incidents_by_month()
    month_rows = [(row["month"], row["month_name"], row["incident_count"])
                  for row in monthly]
    sections.append(dedent(f"""
**3.2 Seasonality**  
_Are incidents more common in certain months or seasons?_

By month:

{md_table(month_rows, ["Month #", "Month", "Incidents"])}

Based on the incident data, wildlife strikes peak in **May** and **September**.  
This pattern is consistent with independent migration data which I found on :

- eBird Status & Trends and BirdCast show the highest migration intensity during late spring (May) and early fall across much of North America.
- USGS waterbird migration studies define spring migration as April–May and fall migration as August–October, bracketing the May and September peaks seen in our dataset.

Although this might feel over generalization since exact timing varies by species and latitude these external data sources support that our “migration" might be causing higher incident in these months.

""").strip())

    return "\n\n---\n\n".join(sections)


template_path = Path(gv.README_TEMPLATE)
output_path = Path(gv.README)

template_text = template_path.read_text(encoding="utf-8")
starting_point = "## Questions & Analyses"

if starting_point not in template_text:
    print(f"Marker {starting_point!r} not found in README.template.md. ")
else:
    insights_md = markdown()
    final_text = template_text.replace(
        starting_point, starting_point + "\n\n" + insights_md)
    output_path.write_text(final_text, encoding="utf-8")
