[![Build Status](https://travis-ci.org/Lagunov-PRO/LP08_Photo_Trail.svg?branch=master)](https://travis-ci.org/Lagunov-PRO/LP08_Photo_Trail)

## Использованные технологии:
* ORM SQLAlchemy
* Yandex Geocoder API
* Pillow 

## Запуск
flask db migrate \
flask db upgrade \
flask run

## Описание
По загруженным фото определяет субъект РФ и закрашивает его на карте РФ # TODO: Мира

## Чему научился
* Получать EXIF информацию из фото (exifread)
* Использовать тег ориентации для поворота фото в правильную сторону (Pillow)
* Создавать миниатюры фотографий (Pillow)
* Поворачивать фотографии по EXIF тегу Orientation (exifread + Pillow)
* Делать авторизацию и регистрацию (miguelgrinberg)
* Оптимально разбивать проект на модули (miguelgrinberg)
* Работать с датой (datetime)
* Импортировать из csv без сохранения файла (io.StringIO)

