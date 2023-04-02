import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def insert_ym(data, client, table_name: str) -> None:

    for row in data.iterrows():
        # prepare a query
        date = row[1]['date']
        traffic_source = row[1]['trafficSource']
        social_network = row[1]['socialNetwork']
        device_category = row[1]['deviceCategory']
        os_root = row[1]['operatingSystemRoot']
        browser = row[1]['browser']
        visits = row[1]['visits']
        pageviews = row[1]['pageviews']
        users = row[1]['users']
        man_percent = row[1]['manPercentage']
        under18_percent = row[1]['under18AgePercentage']
        over44_percent = row[1]['over44AgePercentage']

        # make a check if there is a duplicate
        check_query = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE date = '{date}' AND
                trafficSource = '{traffic_source}' AND
                socialNetwork = '{social_network}' AND
                deviceCategory = '{device_category}' AND
                operatingSystemRoot = '{os_root}' AND
                browser = '{browser}'
            """
        result = client.command(check_query)

        # if there is no duplicates than
        if result == 0:
            # insert the data into the table
            insert_query = f"""
            INSERT INTO {table_name} (date, trafficSource, socialNetwork, deviceCategory,
                                      operatingSystemRoot, browser, visits, pageviews, users,
                                      manPercentage, under18AgePercentage, over44AgePercentage)
                VALUES ('{date}', '{traffic_source}', '{social_network}', '{device_category}',
                        '{os_root}', '{browser}', {visits},
                        {pageviews}, {users}, {man_percent}, {under18_percent}, {over44_percent})
            """
            client.command(insert_query)
            logging.info(f"Data for {date} inserted successfully")
        else:
            logging.info(f"Data for {date} already exists")
