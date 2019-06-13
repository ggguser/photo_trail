from get_coordinates_from_photo import get_exif_location, get_exif_data, get_exif_datetime

image_file = 'IMG_2949.jpg'
exif_data = get_exif_data(image_file)
lat, long = get_exif_location(exif_data)
datetime = get_exif_datetime(exif_data)
print(lat, long)
print(datetime)

