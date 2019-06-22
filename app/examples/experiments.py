from datetime import datetime

from app.get_coordinates import get_exif_date_location, get_exif_data, get_exif_datetime, convert_to_timestamp

image_file = 'IMG_2949.jpg'
exif_data = get_exif_data(image_file)
date_time, lat, long = get_exif_date_location(exif_data)
date_time = get_exif_datetime(exif_data)
dt = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
print(lat, long)
print(date_time)
print(convert_to_timestamp(date_time))
print(dt)
print(dt.timestamp())
print(type(dt))
