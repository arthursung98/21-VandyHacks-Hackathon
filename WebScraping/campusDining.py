from selenium import webdriver
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from time import sleep
import random
from webdriver_manager.chrome import ChromeDriverManager
import json
from unwantedWords import unwantedWords


def scrapeMenus():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    baseURL = 'https://vanderbilt.nutrislice.com/menu/'
    driver.get(baseURL)
    sleep(5)
    button = driver.find_element_by_class_name("primary")
    button.click()
    sleep(5)
    arr = []
    locations = ['2301', 'e-bronson-ingram-dining-hall', 'kissam-dining', 'rand', 'commons-dining', 'zeppos']
    meals = ['breakfast', 'brunch', 'lunch', 'dinner']
    for location in locations:
        link = baseURL + location + '/'
        for meal in meals:
            arr.append({'location': location, 'meal': meal, 'menu': []})
            fullLink = link + meal + '/' + str(date.today())
            driver.set_window_size(720, 600)
            driver.get(fullLink)
            sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            foods = soup.find_all(class_='food-name')
            if (len(foods) > 0):
                for food in foods:
                    if food.text not in unwantedWords:
                        arr[len(arr) - 1]['menu'].append(food.text)
            n = random.randint(5, 15)
            sleep(n)
    driver.quit()
    return arr

# def getMenus():
#     baseURL = 'https://vanderbilt.nutrislice.com/menu/api/digest/school/'
#     file = open('menus' + str(date.today()) + '.txt', 'w')
#     file = open('menus2021-10-08.txt', 'w')
#     locations = ['2301', 'e-bronson-ingram-dining-hall', 'kissam-dining', 'rand', 'commons-dining', 'zeppos']
#     meals = ['breakfast', 'lunch', 'dinner']
#     for location in locations:
#         locLink = baseURL + location + '/menu-type/'
#         file.write(location + '\n\n')
#         for meal in meals:
#             # mealLink = locLink + meal + '/date/' + str(datetime.now().year) + '/' + str(datetime.now().month) + str(datetime.now().day) 
#             mealLink = locLink + meal + '/date/2021/10/08'
#             file.write(meal + '\n')
#             response = requests.get(mealLink)
#             if (response.status_code == 200):
#                 response = response.json()
#                 foods = response["menu_items"]
#                 for food in foods:
#                     file.write(food + '\n')
#                 file.write('\n')
#     file.close()

file = open('DiningLocations.json', 'w')
myArr = json.dumps(scrapeMenus())

json.dump(myArr, file)