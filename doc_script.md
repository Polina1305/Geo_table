### Документация по применению скрипта:

Работа скрипта основана на дообученной модели из sentence-transformers (в основе которой лежит модель LAPSE) путём преобразования названий городов (РФ, Беларусь, Армения, Казахстан, Кыргызстан, Турция, Сербия) и их альтернативных названий в списки вида sentence_transformers.InputExample.

1. Поскольку все модели в Model Hub являются репозиториями Git, вы можете клонировать модели локально, выполнив в терминале по очереди команды:
 
<pre><code>
  git lfs install 
  git clon https://huggingface.co/DataQueen/LAPSE_GEONAMES_RELOC
</code></pre>

2. Для тестирования скрипта script.py, необходимо загрузить необходимое окружение:

<pre><code>
  !pip install -r requirements.txt
</code></pre>
3. Далее осуществить загрузку всех функций, из файла script.py командой:

<pre><code>
  from script import create_connection, query_table, find_similar_labse, result_model
</code></pre>

4. Затем необходимо выполнить следующие команды (эти команды работают только в Jupyter Notebook или IPython.)

<pre><code>
  %load_ext autoreload
  %autoreload 2
</code></pre>

`%load_ext autoreload` - загружает расширение autoreload, которое позволяет автоматически перезагружать измененные модули Python при выполнении кода. Это полезно, когда вы вносите изменения в модуль и хотите, чтобы эти изменения сразу отобразились без необходимости повторной загрузки его вручную.

`%autoreload 2` - настраивает автоматическую перезагрузку для всех модулей. Значение 2 означает, что модули будут автоматически перезагружены, если они были изменены, а если они были удалены или переименованы, то они также будут автоматически перезагружены.

3. Создаём соединение с базой данных PostgreSQL:

`engine = create_connection(name, user, password, host, port, database)`

В случае успешного подключения выводится сообщение "Connection to PostgreSQL DB successful". В случае ошибки выводится сообщение "Ошибка при подключении". Функция возвращает объект engine, представляющий соединение с базой данных.

4. Отбираем данные по необходимым городам релокации.Запрос выполняется командой:

<pre><code>
  names, embeddings, labse = query_table(engine, 'LAPSE_GEONAMES_RELOC')
</code></pre>

Данная функция возвращает массив имен городов, векторные представления городов и модель labse.

5. После создания  списка имена городов, эмбедингов, мы можем рассчитывать косинусное сходство с помощью функции find_similar_labse, в которую необходимо передать название нужного для поиска города:

<pre><code>
  cos_sim = find_similar_labse(city, names, embeddings, labse, top_k)
</code></pre>

6. Для вывода полученного поиска модели в виде списка словарей, мы вызываем функцию  result_model в которую передаём результат 
работы модели(косинусное сходство)

<pre><code>
  result = result_model(cos_sim, engine)
</code></pre>

 8. Результат работы модели выглядит следующим образом для запроса по городу "Брянск", где ключи:
- 'geonameid' : целочисленный идентификатор записи в базе данных geonames 
- 'name' : название географической точки (utf8) varchar(200) 
- 'region': регион нахождения города, (utf8) varchar(200) 
- 'country': название страны (utf8) varchar(200)
- 'cosine_similarity': косинусное сходство, числовое значение рассчитанное моделью на основе заданного запроса 

<pre><code>
  [{'geonameid': 571476,
  'name': 'Bryansk',
  'region': 'Bryansk Oblast',
  'country': 'Russia',
  'cosine_similarity': 0.8491976857185364},
 {'geonameid': 2051523,
  'name': 'Bratsk',
  'region': 'Irkutsk Oblast',
  'country': 'Russia',
  'cosine_similarity': 0.7508770227432251},
 {'geonameid': 1510916,
  'name': 'Barabinsk',
  'region': 'Novosibirsk Oblast',
  'country': 'Russia',
  'cosine_similarity': 0.7139515280723572}]
</code></pre>


<div class="footer">
  &copy; Smol_Pol
</div>
