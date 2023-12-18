## Geo_names
-----------------

### Заказчик:

##### Карьерный центр Яндекс Практикум

----------------------
### Описание проекта:
#### Цель:
- Сопоставление произвольных гео названий с унифицированными именами geonames для внутреннего использования Карьерным центром

---------------------------

#### Задачи:

- Создать решение для подбора наиболее подходящих названий с geonames. Например Ереван -> Yerevan
- На примере РФ и стран наиболее популярных для релокации - Беларусь, Армения, Казахстан, Кыргызстан, Турция, Сербия. Города с населением от 15000 человек (с возможностью масштабирования на сервере заказчика)
- Возвращаемые поля geonameid, name, region, country, cosine similarity
- формат данных на выходе: список словарей, например [{dict_1}, {dict_2}, …. {dict_n}] где словарь - одна запись с указанными полями

-------------------------------

#### Задачи опционально:


- возможность настройки количества выдачи подходящих названий (например в параметрах метода)
- коррекция ошибок и опечаток. Например Моченгорск -> Monchegorsk
- хранение в PostgreSQL данных geonames
- хранение векторизованных промежуточных данных в PostgreSQL
- предусмотреть методы для настройки подключения к БД
- предусмотреть метод для инициализации класса (первичная векторизация geonames)
- предусмотреть методы для добавления векторов новых гео названий

**Используемые таблицы с [GeoNames](http://download.geonames.org/export/dump/):**

- [cities15000.txt](http://download.geonames.org/export/dump/cities15000.txt) - all cities with a population > 15000 or capitals (ca 25.000), see 'geoname' table for columns

- [admin1CodesASCII.txt](http://download.geonames.org/export/dump/admin1CodesASCII.txt) -  names in English for admin divisions. Columns: code, name, name ascii, geonameid

- [alternateNamesV2.zip](http://download.geonames.org/export/dump/alternateNamesV2.zip) -  alternate names with language codes and geonameId, file with iso language codes, with new columns from and to 

- [countryInfo.txt](http://download.geonames.org/export/dump/countryInfo.txt) - country information : iso codes, fips codes, languages, capital ,...
                                
- [geo_test.csv](http://download.geonames.org/export/dump/опаньки_нежданчик)  - to check the operation of our model

### Описание документов проекта: 

  
