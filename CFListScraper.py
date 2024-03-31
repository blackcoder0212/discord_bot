from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
from dotenv import load_dotenv
load_dotenv()
HANDLE = os.getenv('CF_HANDLE')
PASSWORD = os.getenv('CF_PASSWORD')

CFLIST_BASE_URL='https://codeforces.com/list/'
CF_LOGIN='https://codeforces.com/enter'

class ScrapeList():
	def __init__(self):
		opts=Options()
		opts.add_argument("--headless")
		self.browser = Firefox(options=opts)
		self.browser.get(CF_LOGIN)
		sleep(1)
		WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, 'handleOrEmail')))
		self.browser.find_element(By.ID, 'handleOrEmail').send_keys(HANDLE)
		self.browser.find_element(By.ID, 'password').send_keys(PASSWORD)
		self.browser.find_element(By.CLASS_NAME, 'submit').click()
		print("Logged in and Ready:")

	def list_scrape(self,key: str):
		URL = CFLIST_BASE_URL + key
		self.browser.get(URL)
		if self.browser.current_url != URL :
			return ''
		WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rated-user')))
		names = self.browser.find_elements(By.CSS_SELECTOR, '.rated-user')
		ans = ';'.join(name.get_attribute('text') for name in names)
		return ans

	def __del__(self):
		try:
			self.browser.close()
			print("Browser closed:")
		except Exception as e:
			print(f"Error closing browser: {e}")