import requests
from config import supported_countries


def get_json_from_yandex(address: str):
    yandex_maps_url = 'https://geocode-maps.yandex.ru/1.x/'
    # noinspection SpellCheckingInspection
    apikey = '6fc81b5f-cdde-4d9d-bd86-e10e4387bb8a'

    yandex_api_params = {
        'apikey': apikey,
        'format': 'json',
        'geocode': address,
        'kind': 'locality',
        'sco': 'longlat'
    }

    r = requests.get(url=yandex_maps_url, params=yandex_api_params)
    geocoder_info = r.json()
    return geocoder_info


def get_formatted_address(address: str):
    info = get_json_from_yandex(address)
    formatted_address = info['response']['GeoObjectCollection']['featureMember'][0]\
    ['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']

    return formatted_address


def get_country_name(geocoder_info):
    try:
        country_name = geocoder_info['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']\
        ['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']
    except KeyError:
        return None
    return country_name


def get_area_name(geocoder_info):
    try:
        area_name = geocoder_info['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']\
                ['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
    except KeyError:
        return None
    return area_name


def get_city_name(geocoder_info):
    try:
        area_name = geocoder_info['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']\
                ['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
    except KeyError:
        return None
    return area_name


def check_country(country_name):
    for country in supported_countries:
        if country_name == country.name:
            return True
    return False


