#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException

class InstagramBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("C:/Users/James/PycharmProjects/python37/Instagramm/chromedriver/chromedriver")

    #Создаем метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    #Метод для авторизации пользователя
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(3)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    #Метод для поиска и лайка постов
    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(10)

        # цикл для скрола страницы
        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        # соберем все посты (ссылки) со страницы чтобы можно было по ним переходить используем метод поиска по тегу
        hrefs = browser.find_elements_by_tag_name('a')

        # создаем список для ссылок с постами
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        #! цикл обращается к атрибуту href собирает все ссылки из каждого элемента, я это сделал в строче выше более компактно
        # for item in hrefs:
        #     href = item.get_attribute('href')
        #
        #     if "/p/" in href:
        #         posts_urls.append(href)
        #         print(href)

        # пробегаемся по каждой полученной ссылке и ставим лайк
        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(5)

                # ставим лайк
                like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(125, 155))
            except Exception as ex:
                print(ex)
                self.close_browser()

    #Метод для проверки нахождения элемента на стронице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return  exist

    #Cтавим лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(5)

        #если поста не существует
        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует")
            self.close_browser()
        else:
            print("Пост успешно найден")
            time.sleep(3)

            like_button = ('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
            browser.find_element_by_xpath((like_button)).click()
            time.sleep(4)
            print(f"Лайк поставлен: {userpost} поставлен!")
            self.close_browser()

    #Cтавим лайки постов в аккаунте конкретного пользователя
    def put_many_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        # если поста не существует
        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки")
            time.sleep(3)
            #делим кол-во всех постов на странице на 12 для прокрутки
            posts_count = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            #цикл который будет совершать скрол страницы и собирать ссылки
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')

                # создаем список для ссылок с постами
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                #скрол страницы
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2,5))

            #список всех полученых постов сохраняем в фаил
            file_name = userpage.split(("/"))[-2]
            with open(f'{file_name}.txt', 'a') as file:
                for posts_url in posts_urls:
                    file.write(posts_url + '\n')

            #отсортируем задвоиные ссылки на посты в профиле и сохраним в новый фаил
            set_post_urls = set(posts_urls)
            set_post_urls = list(set_post_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for posts_url in set_post_urls:
                    file.write(posts_url + '\n')

            #пройдемся по всем ссылкам и поставим лайк
            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for posts_url in urls_list[0:6]:
                    try:
                        browser.get(posts_url)
                        time.sleep(3)

                        like_button = ('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
                        browser.find_element_by_xpath((like_button)).click()
                        #time.sleep(random.randrange(125, 155))
                        time.sleep(4)
                        print(f"Лайк на пост: {posts_url} успешно поставлен!")
                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()


my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.put_many_likes("https://www.instagram.com/vitaliikingdimov/")
