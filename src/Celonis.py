import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Celonis'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Accept cookies
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located(
			                            (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
	except:
		pass

	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('div', {'class':'vue-table-list__body'})
	jobs = job_table.find_all('a')

	job_list = []
	url = 'https://www.celonis.com'

	if len(jobs) != 0:
		for job in jobs:
			try:
				link = url + job.get('href')
				role = job.find('h2').text.strip()
				location = job.find('div', {'class':'vue-table-list__item__meta'}).text.strip()
				team = job.find_all('div', {'class':'vue-table-list__item__meta'})[1].text.strip()
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

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
