# В этот раз я решил не работать в jupyter notebook по причине
# невозможности работы с отладчиком, а также из-за черезчур большой
# нагрузки на компьютер (selenium слишком много жрет)

#                      *** Задание ***
# Написать программу, которая собирает входящие письма из 
# почтового ящика и сложить данные о письмах в базу данных 
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru

import time
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Определяем коллекцию MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['email']
collection = db.study

# Подгрузим пароль от аккаунта
with open('passwords/lesson_5.txt', 'r') as f:
    password = f.read()[:-1]

# Начнем работу с Selenium
s = Service('./driver/geckodriver')
driver = webdriver.Firefox(service=s)
driver.maximize_window()

driver.get('https://mail.ru/')


# Переходим в поле ввода адреса
elem = driver.find_element(By.XPATH, '//div[contains(@class, "mailbox-services")]/a[3]')
driver.get(elem.get_attribute('href'))
driver.implicitly_wait(15)

# Вводим адрес и переходим в поле ввода пароля
elem = driver.find_element(By.XPATH, './/input[@name="username"]')
elem.send_keys('study.ai_172')
driver.find_element(By.XPATH, './/button[@data-test-id="next-button"]').click()
driver.implicitly_wait(15)

# Вводим пароль и переходим в почту
elem = driver.find_element(By.XPATH, './/input[@name="password"]')
elem.send_keys(password)
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(15)

# Переходим в раздел Почта
elem = driver.find_element(By.XPATH, '//div[contains(@class, "ph-project")]/a[2]')
driver.get(elem.get_attribute('href'))
driver.implicitly_wait(15)

# Прокручиваем страницу до самого низа, пока не загрузим все сообщения
messages_href = set()
while True:
    len_set = len( messages_href )

    # Выделим прокручиваемый блок, что бы использовать в нем PAGE_DOWN
    block = driver.find_element(By.XPATH, '//div[contains(@class, "ReactVirtualized__Grid")]')
    elems = block.find_elements(By.XPATH, './div/a[contains(@class, "llc")]')
    
    for elem in elems:
        messages_href.add( elem.get_attribute('href') )

    if len( messages_href ) == len_set:
        break

    block.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)


# Объявим функцию, генерирующую словарь с нужными данными
def get_insert_dict(driver, href):

    driver.get(href)
    driver.implicitly_wait(15)

    insert_dict = {}

    # email отправителя
    from_mail = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span')
    insert_dict['from_mail'] = from_mail.get_attribute('title')

    # Дата отправления сообщения
    insert_dict['mail_date'] = driver.find_element(By.XPATH, '//div[@class="letter__author"]/div').text

    # Заголовок
    insert_dict['title'] = driver.find_element(By.XPATH, '//h2[@class="thread-subject"]').text

    # Сообщение
    message = driver.find_element(By.XPATH, '//div[@class="letter-body"]').text
    insert_dict['message'] = message
    
    # Текущая дата для ориентирования во времени отправления сообщения
    insert_dict['current_date'] = datetime.now()


    return insert_dict


for href in messages_href:
    insert_dict = get_insert_dict(driver, href)

    collection.insert_one( insert_dict )
