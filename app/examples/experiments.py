from datetime import datetime

from app.exif import get_exif_date_location, get_exif_data, get_exif_datetime, convert_to_timestamp, \
    get_exif_orientation, _get_if_exist

image_file = 'IMG_5542.jpg'
exif_data = get_exif_data(image_file)
date_time, lat, long = get_exif_date_location(exif_data)
date_time = get_exif_datetime(exif_data)
orientation = _get_if_exist(exif_data, 'Image Orientation')
orientation_func = get_exif_orientation(exif_data)
dt = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
print(lat, long)
print(date_time)
print(orientation)
print(orientation_func)
print(convert_to_timestamp(date_time))
print(dt)
print(dt.timestamp())
print(type(dt))
