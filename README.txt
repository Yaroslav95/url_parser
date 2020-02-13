Разработка:
ФИО: Сапронов Ярослав Денисович
EMail: sapr-ya@yandex.ru
Дата: 04.02.2019
----------------------------------------------------------------------------------------------------------------------------------------
Описание:
Программа выполняет обход произвольного сайта с целью найти в его html-коде ссылки url на другие страницы, их заголовки и текст html-страницы. Поиск возможен на различной глубине исходной страницы. Если — depth 0, то сохраняется html, title, url исходного веб-сайта, на каждом depth i+1 дополнительно сохраняются html, title, url с i страницы, и так далее.
Найденная информация загружается в хранилище данных, из которого потом ее можно получить.
----------------------------------------------------------------------------------------------------------------------------------------
Для запуска проекта выполнить следующие действия:

1) Установить следующее программное обеспечение:
   - python3 (https://www.python.org/downloads/), использоваласт версия 3.6.5
   - MySQL (https://dev.mysql.com/downloads/mysql/5.6.html#downloads), использовалась версия 5.6.43 для Windows
   - MySQL Workbench (https://dev.mysql.com/downloads/workbench/), использовалась версия 8.0.15 для Windows
   - Connector/Python (https://dev.mysql.com/downloads/connector/python/8.0.html), использовался mysql-connector-python-8.0.15-py3.7-windows-x86-64bit

2) После установки ПО далее в командной строке перейти в каталог с файлом whl и выполнить pip install url_parser-0.1-py3-none-any.whl
   Выполнить pip install -r requirements.txt для установки зависимостей
   Библиотеки также можно доставить вручную, в случае возникновения ошибок импорта в дальнейшем, например:
   pip install beautifulsoup4
   pip install requests
   pip install memory_profiler
   pip install mysql-connector
  
3) Настроить подключение к серверу MySQL, со следующими параметрами: 
   - Connection Method: Standard (TCP/IP)
   - Hostname: 127.0.0.1
   - Port: 3306
   - Username: root
   - Password: Qwerty123
 
Затем отредактировать файл my.ini/my.cnf (находится в C:\Program Files\MySQL\MySQL Server 5.5): увеличить значение поля max_allowed_packet, например = 219430400 
Либо через интерфейс MySQL Workbench перейти в настройки сервера (INSTANCE/Options file/Networking/max_allowed_packet) и изменить значение max_allowed_packet.
Это необходимо для увеличения пропускной способности и загрузки информации в базу данных в рамках одного подключения к базе данных.

4) Из MySQL Workbench выполнить скрипт create_table.sql (Создает базу данных news_parser и таблицу url_information)

5) Запустить файл cmd_run.py (в командной строке перейти в каталог, куда был помещен файл)
   Выполнить команду запуска по примеру:
   python cmd_run.py load http://tass.ru/ural 1 (загрузка данных с сайта в хранилище на глубине 1)
   python cmd_run.py get http://tass.ru/ural 20 (получение данных из хранилища в количестве 20 строк)


