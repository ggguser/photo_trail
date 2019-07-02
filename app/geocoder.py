import requests


def get_json_from_yandex(address: str):
    yandex_maps_url = 'https://geocode-maps.yandex.ru/1.x/'
    # noinspection SpellCheckingInspection
    apikey = '6fc81b5f-cdde-4d9d-bd86-e10e4387bb8a'

    yandex_api_params = {
        'apikey': apikey,
        'format': 'json',
        'geocode': address
    }

    r = requests.get(url=yandex_maps_url, params=yandex_api_params)
    geocoder_info = r.json()
    return geocoder_info


def get_formatted_address(address: str):
    info = get_json_from_yandex(address)
    formatted_address = info['response']['GeoObjectCollection']['featureMember'][0]\
    ['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']

    return formatted_address


def get_area_name(address: str):
    info = get_json_from_yandex(address)
    area_name = \
    info['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']\
        ['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']

    return area_name
