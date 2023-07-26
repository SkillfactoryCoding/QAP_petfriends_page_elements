import chromedriver_autoinstaller

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Для пользователей Windows
chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()

   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')

   driver.maximize_window()
   yield driver

   driver.quit()


def test_show_all_pets(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys('delich@gmail.com')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # список всех обьектов питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: 'Мурзик Котэ 5'
   all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

   # этот список image объектов , который имееют метод get_attribute('src') ,
   # благодаря которому можно посмотреть есть ли изображение питомца или нет.
   all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')

   # проверяем что список своих питомцев не пуст
   assert len(all_my_pets) > 0

   pets_info = []
   for i in range(len(all_my_pets)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # избавляемся от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
      pets_info.append(pet_info)
