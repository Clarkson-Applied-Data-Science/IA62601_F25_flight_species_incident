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
