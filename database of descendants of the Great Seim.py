
import os
from selenium import webdriver
from bs4 import BeautifulSoup as b 
import time 
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
import string
from textblob import TextBlob
import multiprocessing
import requests


while True:
	try:
		#Useragent
		user_agent = UserAgent()
		#Webdriver
		options = webdriver.FirefoxOptions()
		#options.add_argument("--disable-blink-features=AutomationControlled")
		#options.headless = True
		options.add_argument(f"user_agent={user_agent.ie}")
		driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)
		wait = WebDriverWait(driver, 20)
		

		href_all = []

		#Search
		def parser():
			global href_all
			driver.get(url="http://www.sejm-wielki.pl/")
			qests = str(input("Enter first and last name "))
			driver.find_element(By.XPATH, "/html/body/form/input[1]").send_keys(qests)
			driver.find_element(By.XPATH, "/html/body/form/input[2]").click()
			screen = driver.page_source
			
			def check():
				try:
					driver.find_element(By.XPATH,"/html/body/h2[1]")
				except Exception as exc:
					return False
				return True

			check()
			result = check()
		
			if result == True:
				soup = b(screen, "html.parser")
				href = soup.find('ul')
				a = ""
				for i in href.find_all('a', href=True):
					a = a+','+'http://www.sejm-wielki.pl/'+(i['href'])
				href_all = a.split(',')
				#Все ссылки
				del href_all[1]		
			else:
				soup = b(screen, "html.parser")
				data_sup = soup.find('ul').text
				data = data_sup.replace("All sources for this personAdd or correct dates and places", "")
				#Перевод текста библиотека TextBlob
				blob = TextBlob(str(data))
				res = blob.translate(from_lang='pl', to='en')
				print(res)
		parser()

		print(href_all)
		gggg = ['http://www.sejm-wielki.pl//b/ut.1.1.229', 'http://www.sejm-wielki.pl//b/cz.I004982', 'http://www.sejm-wielki.pl//b/sw.59095']
		def get_data(url):
			r = requests.get(url)
			soup = b(r.text, "html.parser")
			data_sup = soup.find('ul').text
			data = data_sup.replace("All sources for this personAdd or correct dates and places", "")
			print(data)


		with multiprocessing.Pool(processes=3) as process:
			process.map(get_data, gggg)

		driver.close()
		driver.quit()

	except Exception as ex:
		print(ex)
		driver.close()
		driver.quit()
		break

