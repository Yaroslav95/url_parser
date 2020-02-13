#Сапронов Ярослав// 03.02.2019
#-*- coding: UTF-8 -*-
#импорт библиотеки получения параметров из командной строки
from sys import argv

#импорт библиотек для считывания времени и памяти
import time
from memory_profiler import memory_usage

#импорт библиотек парсинга web-страниц
from bs4 import BeautifulSoup
import requests

#Импорт библиотек соединения с базой и возникающих ошибок
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

#Входные параметры из командной строки
script_name, func, url, count  = argv

"""
Функция parsing_web_pages выполняет обход произвольного сайта с целью найти в его html-коде ссылки url на другие страницы,
их заголовки и текст html-страницы. Поиск возможен на различной глубине исходной страницы. Если — depth 0, то сохраняется html,
title, url исходного веб-сайта, на каждом depth i+1 дополнительно сохраняются html, title, url с i страницы, и так далее.

На вход принимает 2 параметра: url (ссылка исходного веб-сайта) и depth (глубина поиска)
В качестве примера url: https://ria.ru/, http://www.vesti.ru/, http://echo.msk.ru/, http://tass.ru/ural, https://lenta.ru/)
depth: 0,1,2

На выходе функция возвращает 3 списка urls, titles, html_pages, содержащие найденные url, title, html
"""

def parsing_web_pages(url, depth):
    html_pages = []  #Список для хранения html кода страниц
    titles = []  #Список для хранения заголовков страниц
    urls = []  #Список для хранения ссылок страниц
    #Цикл выполняет поиск по каждой глубине
    for dp in range(0, depth + 1):
        cur_links = [] #Список ссылок, который будет обрабатываться на текущей глубине, очищается в начале
        #Если глубина = 0, то в список cur_links добавляем только одну ссылку исходного веб-сайта
        if (dp == 0):
            cur_links = [url]
        #Иначе в список cur_links добавляются ссылки (без дублей) из списка new_links, полученном на предыдущей глубине
        else:
            cur_links = set(new_links)  
        
        new_links = []  #Список новых ссылок очищается для повторного использования на текущей глубине
        #Цикл перебирает все ссылки в списке рассмативаемых на текущей глубине
        for link in cur_links:
            #В случае исключительной ситуации переход в блок except
            try:
                req = requests.get(link)  #Получение ответа по ссылке
                req.encoding = 'utf8'  #Для считывания русских символов используется кодировка utf-8
                html = BeautifulSoup(req.text, "lxml")  #С помощью BeautifulSoup получаем текст html страницы в формате lxml
                title = html.find('title').text  #Поиск заголовка в html      
                html_str = str(html)  #Преобразование html-кода в строку
                urls.append(link)  #Добавление ссылки рассматриваемой html страницы в выходной список
                titles.append(title)  #Добавление заголовка рассматриваемой html страницы в выходной список 
                html_pages.append(html_str)  #Добавление текста рассматриваемой html страницы в выходной список 
                               
                #Условие определяет, будет ли еще одна глубина, и соответственно, нужны ли новые ссылки
                if (dp < depth): 
                    #В цикле осуществляется поиск по тегу 'a' ссылок на рассматриваемой html-странице
                    for href in html.find_all('a', href = True):
                        #В случае исключительной ситуации переход в блок except
                        try:
                            new_link = href.get('href') #Из содержания тега 'a' извлекается текст 'href'
                            #Условие проверяет, что полученный 'href' не пустой
                            if (len(new_link) > 1):
                                #Условие проверяет, что ссылка начинается с 'http' и не оканчивается на '.mp3' и т.д для фильтрации медиа контента
                                #if (new_link[0] not in ('/', '#', '?')):
                                if (new_link[:4] == 'http' and new_link[len(new_link)-4:] not in ('.mp3', '.jpg', '.mp4', '.gif')):
                                    new_links.append(new_link)  #Добавление ссылки в список для следующей глубины 
    
                        #Если было исключение, то переход к следующей итерации цикла
                        except Exception as ex_1:
                            #print('Ошибочный переход по ссылке ', href)
                            #print(ex_1)
                            pass
            
            #Если было исключение, то переход к следующей итерации цикла
            except Exception as ex_2:
                #print('Невозможно разобрать ссылку ', link)
                #print(ex_2)
                pass
        
        cur_links = [] #Очистка cur_links
    
    return (urls, titles, html_pages)  

"""
Функция load_information выполняет соединение к базе данных MySQL и затем загружает в таблицу базы данных url, title, html, 
полученные в функции парсера parsing_web_pages.

На вход принимает 1 параметр: parsing_res (результат парсера parsing_web_pages).
На выходе функция информирует о том, что данные успешно загружены, или, при возникновении ошибки, ее подробности.
"""

def load_information(parsing_res):
    #В случае исключительной ситуации переход в блок except
    try:
        #Настраиваются параметры подключения к базе данных
        connection = mysql.connector.connect(host='localhost',
                                 database='news_parser',
                                 user='root',
                                 password='Qwerty123',
                                 charset = 'utf8')  #utf8mb4
        
        print("Соединение открыто") 
        cnt_insert = 0  #Количество вставленных записей
        
        #Цикл построчно проходит кортеж (url, title, html), полученный в резульате парсинга web-страниц 
        for i in range (0, len(parsing_res[0])): 
            #В случае исключительной ситуации переход в блок except
            try:
                #В переменной records_to_insert формируется строка загрузки в базу данных
                records_to_insert = [(parsing_res[0][i], parsing_res[1][i], parsing_res[2][i], parsing_res[0][0])]
                #В переменной sql_insert_query формируется запрос вставки в базу данных
                sql_insert_query = """ INSERT INTO `url_information`
                                       (`url`, `title`, `html_code`, `url_parent`) VALUES (%s, %s, %s, %s);"""
                cursor = connection.cursor()  #Создание курсора для текущего соединения
                result  = cursor.executemany(sql_insert_query, records_to_insert)  #Вставка записи из нескольких столбцов в базу
                connection.commit()  #Подтверждение загрзуки
                cnt_insert = cnt_insert + 1
        
            #Если запись не может быть вставлена в базу данных, то переход к следующей итерации цикла 
            except Exception as ex_3:
                #print('Не добавлена ссылка ', parsing_res[0][i])
                #print(ex_3)
                pass
    
        print ("Операция вставки выполнена, количество новых строк: ", cnt_insert)
        
    #Если была ошибка подключения, то выводится информация по ошибке
    except mysql.connector.Error as error :
        print("Ошибка вставки записей в таблицу {}".format(error))
    
    #Завершение операций вставки и подключения
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Соединение закрыто")      
			
"""
Функция load_information выполняет соединение к базе данных MySQL и затем загружает в таблицу базы данных url, title, html, 
parent_html, полученные в функции парсера parsing_web_pages.
В данном случае parent_html - это родительская ссылка (глубина 0), на следующей глубине все ссылки также будут иметь parent_html
с глубины 0. Это необходимо для дальнейших запросов к базе данных по уже загруженным записям.

На вход принимает 1 параметр: parsing_res (результат парсера parsing_web_pages).
На выходе функция информирует о том, что данные успешно загружены, или, при возникновении ошибки, ее подробности.
"""

def get_information(get_url, cnt_row):
    #В случае исключительной ситуации переход в блок except
    try:
        #Настраиваются параметры подключения к базе данных
        connection = mysql.connector.connect(host='localhost',
                                 database='news_parser',
                                 user='root',
                                 password='Qwerty123',
                                 charset = 'utf8')  #utf8mb4
        
        #print("Соединение открыто") 
        cursor = connection.cursor()
        #В переменной sql формируется запрос строк по родительским ссылкам с ограничением до cnt_row записей
        sql_select = """SELECT url, title FROM url_information
                        WHERE url_parent = %s
                        LIMIT %s"""       
        result  = cursor.execute(sql_select, (get_url, cnt_row))  #Выборка нескольких строк из базы
        row = cursor.fetchone()  #Устанавливаем курсор на первую запись
        
        #В цикле последовательно рассматриваются все записи, полученные в результате запроса в базу дааных
        while row is not None:
            str_sql_url = str(row[0])  #Строка url для вывода в интерфейс
            str_sql_title = str(row[1])  #Строка title для вывода в интерфейс
            print(str_sql_url + ': ' + str_sql_title)
            row = cursor.fetchone()   #Переход к следуюющей строке       
           
    #Если была ошибка подключения, то выводится информация по ошибке
    except mysql.connector.Error as error :
        print("Ошибка выборки записей из таблицы {}".format(error))
    
    #Завершение операций вставки и подключения
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            #print("Соединение закрыто")  			
			
"""
Функция main_func является главной функцией, включает все остальные. Здесь происходит вызов функции парсинга веб-сайта и 
загрузки полученной информации в базу данных, а также есть функция запроса и отображения загруженных записей в базу данных.
main_func включает таймер выполнения и счетчик используемой памяти при вызове функций.

На вход принимает 4 параметра: script_name (имя исходного скрипта), func(загрузить в базу или получить уже загруженные
данные), url(ссылка на web-сайт для обработки), count(глубина или количество отображаемых строк из базы, в зависимости
от функции).
В результате main_func выполняет необходимые функции, которые имеют свои выходные данные. Также main_func показывает
время выполнения и объем задействованной памяти, а при возникновении ошибки, ее подробности.
"""
	
def main_func(script_name, func, url, count):	
    start_time = time.time()  #Запуск таймера  
    count = int(count)  #Глубина или счетчик записей
		
    #В условии проверяется, если запрошена функция загрузки, то вызываются соответствующие функции, глубина = count
    if (func == 'load'):
        parsing_res = parsing_web_pages(url, count)  #Парсинг web-сайта
        load_information(parsing_res)  #Загрузка в базу данных
        print ('ok, execute time: %s seconds' %(time.time() - start_time))
        memory = memory_usage()  #Счетчик используемой памяти
        print("Объем занимаемой памяти %s Mb" % memory)        
        
    #В условии проверяется, если запрошена функция отображения, то вызываются соответствующие функции, количество строк = count
    if (func == 'get'):
        get_information(url, count)  #Отображение записей из базы
	
    #Если ошибка ввода функции, то предупреждение, а другие ошибки обрабатываются в функциях 
    if (func != 'get' and func != 'load'):
        print('Ошибка обработки запроса, проверьте введенные данные по примеру cmd_run.py load(get) http://www.vesti.ru/ 2')
		
		
#Вызов функции, включающей весь функционал
main_func(script_name, func, url, count)	
	
