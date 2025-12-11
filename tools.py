from math import radians, sin, cos, asin, sqrt
import pymysql
import yaml
from pathlib import Path

config = yaml.safe_load(Path('config.yml').read_text())


def connect_to_db():
    conn = pymysql.connect(host=config['db']['host'], port=3306, user=config['db']
                           ['user'], passwd=config['db']['pw'], db=config['db']['db'], autocommit=True)
    return conn.cursor(pymysql.cursors.DictCursor)


def str_to_float_convertor(to_be_converted):
    val = None
    try:
        val = float(to_be_converted)
    except Exception as e:
        pass
        # print(to_be_converted, e)
    return val


def str_to_int_convertor(to_be_converted):
    val = None
    try:
        val = int(to_be_converted)
    except Exception as e:
        pass
        # print(to_be_converted,e)
    return val


def batch_reader(file_path, batch_size=10):
    with open(file_path, 'r') as f:
        batch = []
        for line in f:
            batch.append(line)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(float, (lat1, lon1, lat2, lon2))
    R_of_Earth = 3958.8
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R_of_Earth * c
