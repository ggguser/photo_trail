import csv
from distutils.util import strtobool


def read_csv(csv_import_file):

    with open(csv_import_file, newline='', encoding='utf-8-sig') as csv_file:
        csv_import = csv.DictReader(csv_file, delimiter=';')

        #  Processing the dict, converting values to appropriate types
        country_import = []
        for data in csv_import:
            data['name'] = str(data['name'])
            data['iso'] = str(data['iso'])

            country_import.append(data)
    return country_import


def areas_csv_import(filename):

    with open(filename, newline='', encoding='utf-8-sig') as csv_file:
        csv_import = csv.reader(csv_file, delimiter=';')
        #  Composing the dict, converting values to appropriate types
        areas_csv_import = {area[0]: str(area[1]) for area in csv_import}

    return areas_csv_import