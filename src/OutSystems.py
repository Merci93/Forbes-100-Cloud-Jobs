import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'OutSystems'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
	except:
		pass

	# Open positions
	pos = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			(By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/div/div/div/div[2]/div/a'))).get_attribute('href')
	driver.get(pos)

	job_list = []

	while True:
		# Wait for page to load
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thin')))
		jobs = driver.find_elements(By.CLASS_NAME, 'thin')

		if len(jobs) != 0:
			for i in range(2, len(jobs) + 2):
				role = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/table/tbody/tr['
											+ str(i) + ']/td[1]/a').text
				link = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/table/tbody/tr['
											+ str(i) + ']/td[1]/a').get_attribute('href')
				team = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/table/tbody/tr['
											+ str(i) + ']/td[2]').text
				location = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/table/tbody/tr['
												+ str(i) + ']/td[3]').text
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			# Next page
			try:
				driver.find_element(By.LINK_TEXT, 'Next').click()
			except:
				break
		else:
			print(company_name + ': No data obtained')
			break

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()

