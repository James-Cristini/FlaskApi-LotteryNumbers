# ~ https://catalog.data.gov/dataset/lottery-powerball-winning-numbers-beginning-2010
    ### https://data.ny.gov/api/views/d6yy-54nr/rows.csv?accessType=DOWNLOAD
# ~ https://catalog.data.gov/dataset/lottery-mega-millions-winning-numbers-beginning-2002
    ### https://data.ny.gov/api/views/5xaw-6ayf/rows.csv?accessType=DOWNLOAD

import pandas as pd
import requests
import json
import argparse

import date_helpers

POWERBALL_FILE = 'src/helpers/powerball_dataset.csv'
MEGAMILLIONS_FILE = 'src/helpers/megamillions_dataset.csv'

POWERBALL_URL = 'http://127.0.0.1:5000/powerball'
MEGAMILLIONS_URL = 'http://127.0.0.1:5000/megamillions'


def fix_date(dt):

    dt = date_helpers.str_to_dto(dt)
    dt = date_helpers.dto_to_str(dt)
    return dt


def get_and_load_powerball_data():
    try: # Load dataframe from csv
        df = pd.read_csv(POWERBALL_FILE)
    except IOError:
        raise # TODO look for and download file, then load dataframe

    ### Get most recent date in exiting API data
    last_draw_date = get_most_recent_date('powerball')

    ### Fix date columns
    df['Draw Date'] = df['Draw Date'].apply(fix_date)

    ### Filter new data to only include newer drawings
    df = df[df['Draw Date'] > last_draw_date]

    for index, row in df.iterrows():

        # Parse out cell data
        draw_date = row['Draw Date']
        numbers_list = row['Winning Numbers']
        multiplier = row['Multiplier']

        # Get numbers from string
        n1, n2, n3, n4, n5, pb = numbers_list.split(' ')

        # Fix date format # XXX Uncessecary now
        # draw_date = date_helpers.str_to_dto(draw_date)
        # draw_date = date_helpers.dto_to_str(draw_date)

        # Create json data object
        data = {
            "draw_date": draw_date,
            "number_1": n1,
            "number_2": n2,
            "number_3": n3,
            "number_4": n4,
            "number_5": n5,
            "powerball_number": pb,
            "multiplier": multiplier
        }

        # Send API post request
        requests.post(POWERBALL_URL, json=data)
        print "Powerball drawing data sent: {0}".format(data) # TODO convert to logging


def get_and_load_megamillions_data():
    try: # Load dataframe from csv
        df = pd.read_csv(MEGAMILLIONS_FILE)
    except IOError:
        raise # TODO look for and download file, then load to dataframe

    ### Get most recent date in exiting API data
    last_draw_date = get_most_recent_date('megamillions')

    ### Fix date columns
    df['Draw Date'] = df['Draw Date'].apply(fix_date)

    ### Filter new data to only include newer drawings
    df = df[df['Draw Date'] > last_draw_date]

    for index, row in df.iterrows():

        # Parse out cell data
        draw_date = row['Draw Date']
        numbers_list = row['Winning Numbers']
        mb = row['Mega Ball']
        multiplier = row['Multiplier']

        # Fix numbers from string
        n1, n2, n3, n4, n5 = numbers_list.split(' ')

        # Fix date format
        draw_date = date_helpers.str_to_dto(draw_date)
        draw_date = date_helpers.dto_to_str(draw_date)

        # Create json data object
        data = {
            "draw_date": draw_date,
            "number_1": n1,
            "number_2": n2,
            "number_3": n3,
            "number_4": n4,
            "number_5": n5,
            "megaball_number": mb,
            "multiplier": multiplier
        }

        requests.post(MEGAMILLIONS_URL, json=data)
        print "Megamillion drawing data sent: {0}".format(data) # TODO convert to logging

DRAWINGS = {
    'powerball': get_and_load_powerball_data,
    'pb': get_and_load_powerball_data,
    'megamillions': get_and_load_megamillions_data,
    'mm': get_and_load_megamillions_data,
}

def get_most_recent_date(pb_or_mm):
    """ """
    # Get and update url based on param
    url = POWERBALL_URL if pb_or_mm == 'powerball' else MEGAMILLIONS_URL if pb_or_mm == 'megamillions' else ''
    url += '/last_drawing'
    # Get last drawing object
    req = requests.get(url)
    last_drawing = json.loads(req.content)[0]
    last_date = last_drawing['draw_date']

    return last_date


def run(drawing):
    try: # Attempt to run function
        func = DRAWINGS[drawing]
        func()
    except KeyError:
        raise ValueError('Drawing {0}, is not a valid drawing name, valid drawings are:\n{1}'.format(drawing, ', '.join(DRAWINGS)))

def parse_cl_args():
    """ Parses command line arguments and returns them as a dictionary """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process input arguments')

    # Add command line arguments
    parser.add_argument('drawing', metavar='Input', type=str, nargs=1,
            help='Expects a single argument of "powerball" or "megamillions"')

    # Send command line arguments to dict
    cl_args = vars(parser.parse_args())

    # Since nargs puts this arg in a list, need to pull it out
    cl_args['drawing'] = cl_args['drawing'][0]

    return cl_args

if __name__ == '__main__':
    # cl_args = parse_cl_args()
    # drawing = cl_args['drawing']
    # run(drawing)
    get_and_load_megamillions_data()
