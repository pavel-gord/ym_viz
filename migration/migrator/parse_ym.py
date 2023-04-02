import sys
import logging
import pandas as pd
import requests
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_metrics(dims: list) -> str:
    """This function takes a list of metric names and returns a string with the metrics in the
    format expected by the Yandex.Metrica API. The returned string includes the prefix
    "ym:s:" for each metric name."""
    
    return ''.join(['metrics='] + ['ym:s:' + i + ',' for i in dims])[:-1]


def create_dimensions(dims: list) -> str:
    """This function takes a list of dimension names and returns a string with the dimensions in
    the format expected by the Yandex.Metrica API. The returned string includes the prefix
    "ym:s:" for each dimension name."""

    return ''.join(['dimensions='] + ['ym:s:' + i + ',' for i in dims])[:-1]


def transform_ym_json(json_data: dict):
    """This function takes a JSON object returned by the Yandex.Metrica API and transforms it into
    a Pandas DataFrame. ."""
    
    # make headers for the future table
    dimensions = [i[5:] for i in json_data['query']['dimensions']]
    metrics = [i[5:] for i in json_data['query']['metrics']]
    headers = dimensions + metrics

    # transform to pandas df
    data = pd.DataFrame()
    for n, values  in enumerate(json_data['data']):
        row = ([i['name'] for i in json_data['data'][n]['dimensions']]  +  # dimensions
               [i for i in json_data['data'][n]['metrics']])               # metrics
        data = pd.concat([data, pd.DataFrame(row).T])
    data.columns = headers

    return data.fillna('n/a')


def get_ym_data(start_date, end_date):
    """This function constructs the URL for the Yandex.Metrica API request, sends the request,
    and returns the transformed Pandas DataFrame using the transform_ym_json function."""

    # parameters
    counter_id = 'id=44147844'
    metrics = ['visits', 'pageviews', 'users', 'manPercentage',
               'under18AgePercentage', 'over44AgePercentage']
    dimensions = ['date', 'TrafficSource', 'SocialNetwork',
                  'deviceCategory', 'operatingSystemRoot', 'browser']
    date_range = f'date1={start_date}' + '&' + f'date2={end_date}'
    limit = 'limit=100000'

    # construct url
    BASE_URL = 'https://api-metrika.yandex.net/stat/v1/data?'
    url = (BASE_URL + counter_id + '&' +
           create_metrics(metrics) + '&' +
           create_dimensions(dimensions) + '&' +
           date_range + '&' + limit)

    # get json of response
    logging.info(f'Sending request to {url}')
    query = requests.get(url)

    if query.status_code == 200:
        logging.info('Request is accepted')
    else:
        logging.error('Request is not accepted!')

    json_data = json.loads(query.text)

    return transform_ym_json(json_data)

# start the script
if __name__ == '__main__':
    print(get_ym_data('400daysAgo', 'yesterday').head(10))