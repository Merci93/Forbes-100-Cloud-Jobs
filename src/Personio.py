import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Personio'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		time.sleep(2)
		query = '''return document.querySelector("#usercentrics-root").shadowRoot.querySelector("button[data-testid='uc-accept-all-button']")'''
		accept_all = driver.execute_script(query)
		accept_all.click()
	except:
		print('No cookies found')
		pass

	# load all open positions
	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
											(By.XPATH, '//*[@id="button-load-more"]'))).click()
		except:
			break

	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find_all('div', {'class':'lg:col-start-2 lg:col-end-12 col-span-full'})[2]
	jobs = job_table.find_all('div', {'class':'grid-cols-10'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			try:
				team = 'N/A'
				link = job.find('a', {'data-component-id':'C003'}).get('href')
				role = job.find('div', {'class':'md:col-span-4 xs:col-span-8 font-bold truncate ...'}).text.replace('#', '')
				location = job.find('div', {'class':'md:border-0'}).text
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			except:
				continue
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list, columns = columns)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()

