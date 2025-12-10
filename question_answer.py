import yaml
from pathlib import Path
from tools import config, connect_to_db
import json
config = yaml.safe_load(Path('config.yml').read_text())
cur = connect_to_db()


def q_1b_species_level_frequency(low_n=10):
    sql = f"""
        SELECT s.sid, s.species_name, s.class AS taxonomic_class, COUNT(*) AS incident_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['species']} AS s
        ON i.species_id = s.sid
        GROUP BY s.sid, s.species_name, s.class
        ORDER BY incident_count ASC
        LIMIT %s;
    """
    cur.execute(sql, (low_n,))
    return cur.fetchall()


def q_1_species_level_frequency(top_n=10):
    sql = f"""
        SELECT s.sid, s.species_name, s.class AS taxonomic_class, COUNT(*) AS incident_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['species']} AS s
        ON i.species_id = s.sid
        GROUP BY s.sid, s.species_name, s.class
        ORDER BY incident_count DESC
        LIMIT %s;
    """
    cur.execute(sql, (top_n,))
    return cur.fetchall()


# print(json.dumps(q_1_species_level_frequency(), indent=2, default=str))


def q_2_class_level_patterns(top_n=10):
    sql = f"""
        SELECT s.class AS taxonomic_class, COUNT(*) AS incident_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['species']} AS s
        ON i.species_id = s.sid
        GROUP BY s.class
        ORDER BY incident_count DESC
        LIMIT %s;
    """
    cur.execute(sql, (top_n,))
    return cur.fetchall()

# print(json.dumps(q_2_class_level_patterns(), indent=2, default=str))


def q_3_species_airport_spread(top_n=10):
    sql = f"""
        SELECT
            s.sid,
            s.species_name,
            s.class,
            COUNT(DISTINCT i.airport_id) AS airport_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['species']} AS s
          ON i.species_id = s.sid
        GROUP BY s.sid, s.species_name, s.class
        ORDER BY airport_count DESC
        LIMIT %s;
    """
    cur.execute(sql, (top_n,))
    return cur.fetchall()

# print(json.dumps(q_3_species_airport_spread(), indent=2, default=str))


def q_4_airport_risk(top_n=10):
    cur = connect_to_db()
    sql = f"""
        SELECT
            a.aid,
            a.name AS airport_name,
            a.icao,
            COUNT(*) AS incident_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['airport']} AS a
          ON i.airport_id = a.aid
        GROUP BY a.aid, a.name, a.icao
        ORDER BY incident_count DESC
        LIMIT %s;
    """
    cur.execute(sql, (top_n,))
    return cur.fetchall()


# print(json.dumps(q_4_airport_risk(), indent=2, default=str))

def q_5_airline_incident_counts(top_n=10):
    cur = connect_to_db()
    sql = f"""
        SELECT
            al.aid,
            al.airline,
            al.icao,
            COUNT(*) AS incident_count
        FROM {config['tables']['incident']} AS i
        JOIN {config['tables']['airline']} AS al
          ON i.operator_id = al.aid
        GROUP BY al.aid, al.airline, al.icao
        ORDER BY incident_count DESC
        LIMIT %s;
    """
    cur.execute(sql, (top_n,))
    return cur.fetchall()
# print(json.dumps(q_5_airline_incident_counts(), indent=2, default=str))


def q_6_trends_over_time_by_year():
    cur = connect_to_db()
    sql = f"""
        SELECT
            YEAR(incident_date) AS year,
            COUNT(*) AS incident_count
        FROM {config['tables']['incident']}
        GROUP BY YEAR(incident_date)
        ORDER BY incident_count DESC;
    """
    cur.execute(sql)
    return cur.fetchall()


# print(json.dumps(q_6_trends_over_time_by_year(), indent=2, default=str))

def q_7_incidents_by_month():
    cur = connect_to_db()
    sql = f"""
        SELECT
            MONTH(incident_date)        AS month,
            MONTHNAME(incident_date)    AS month_name,
            COUNT(*)                    AS incident_count
        FROM {config['tables']['incident']}
        GROUP BY MONTH(incident_date), MONTHNAME(incident_date)
        ORDER BY incident_count DESC;
    """
    cur.execute(sql)
    return cur.fetchall()


# print(json.dumps(q_7_incidents_by_month(), indent=2, default=str))
