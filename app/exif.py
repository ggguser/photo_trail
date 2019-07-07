import exifread
from datetime import datetime
import time
from PIL import Image
import os


def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lng = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degrees(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lng = _convert_to_degrees(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lng = 0 - lng

        lat = round(lat, 6)
        lng = round(lng, 6)

    return lat, lng


def get_exif_orientation(exif_data):
    """
        1: 'Horizontal (normal)',
        2: 'Mirrored horizontal',
        3: 'Rotated 180',
        4: 'Mirrored vertical',
        5: 'Mirrored horizontal then rotated 90 CCW',
        6: 'Rotated 90 CW',
        7: 'Mirrored horizontal then rotated 90 CW',
        8: 'Rotated 90 CCW'
    """
    orientation = _get_if_exist(exif_data, 'Image Orientation')

    return orientation


def create_thumbnail(photo, thumbnail, size, orientation):
    with open(photo, 'rb') as photo_file:
        im = Image.open(photo_file)
        if orientation:
            if 1 in orientation.values:
                pass
            elif 3 in orientation.values:
                im = im.rotate(180, expand=True)
            elif 6 in orientation.values:
                im = im.rotate(270, expand=True)
            elif 8 in orientation.values:
                im = im.transpose(Image.ROTATE_90)

        im.thumbnail(size, Image.ANTIALIAS)
        im.save(thumbnail, "JPEG", quality=80)


def get_exif_datetime(exif_data):
    photo_datetime = _get_if_exist(exif_data, 'Image DateTime')
    if photo_datetime:
        return datetime.strptime(photo_datetime.values, '%Y:%m:%d %H:%M:%S')
    return None

