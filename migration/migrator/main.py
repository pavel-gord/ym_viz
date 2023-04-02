import os
import parse_ym
import clickhouse_connect
import queries

def main():
    start_date = os.environ.get('START_DATE')
    end_date = os.environ.get('END_DATE')

    ch_host = os.environ.get('CLICKHOUSE_HOST')
    ch_db = os.environ.get('CLICKHOUSE_DB')
    ch_table = os.environ.get('CLICKHOUSE_TABLE')
    ch_username = os.environ.get('CLICKHOUSE_USER')
    ch_password = os.environ.get('CLICKHOUSE_PASSWORD')
    ch_port = os.environ.get('CLICKHOUSE_PORT')

    data = parse_ym.get_ym_data(start_date, end_date)

    client = clickhouse_connect.get_client(host=ch_host,
                                           database=ch_db,
                                           username=ch_username,
                                           password=ch_password,
                                           port=ch_port)

    # load initial data from yandex metrics
    queries.insert_ym(data, client, ch_table) # type: ignore

# start the script
if __name__ == '__main__':
    main()
