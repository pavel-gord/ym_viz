import sys
import logging
import os
import parse_ym
import clickhouse_connect
import queries

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info('Starting migration...')

    # set initial data range
    start_date = os.environ.get('START_DATE')
    end_date = os.environ.get('END_DATE')

    # get info about the db
    ch_host = os.environ.get('CLICKHOUSE_HOST')
    ch_db = os.environ.get('CLICKHOUSE_DB')
    ch_table = os.environ.get('CLICKHOUSE_TABLE')
    ch_username = os.environ.get('CLICKHOUSE_USER')
    ch_password = os.environ.get('CLICKHOUSE_PASSWORD')
    ch_port = os.environ.get('CLICKHOUSE_PORT')

    # download data from yandex metrics
    logging.info('Downloading data from Yandex Metrics')
    data = parse_ym.get_ym_data(start_date, end_date)

    # login into the db
    logging.info(f'Connecting to the database {ch_db} with port {ch_port} as {ch_username}')
    client = clickhouse_connect.get_client(host=ch_host,
                                           database=ch_db,
                                           username=ch_username,
                                           password=ch_password,
                                           port=ch_port)

    # load initial data to the db
    logging.info('Loading data to the database')
    try:
        queries.insert_ym(data, client, ch_table) # type: ignore
        logging.info('Loading succeed')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# start the script
if __name__ == '__main__':
    main()
