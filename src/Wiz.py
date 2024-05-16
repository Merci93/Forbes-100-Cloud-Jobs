import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Wiz'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
			                           (By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
	except:
		pass

	# Open positions
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
									(By.LINK_TEXT, 'See open positions'))).click()

	search_body = bs(driver.page_source, 'html.parser')
	job_table = search_body.find('ul', {'class':'divide-y divide-gray-100'})
	jobs = job_table.find_all('li')

	job_list = []
	url = 'https://www.wiz.io'

	if len(jobs) != 0:
		for job in jobs:
			try:
				team = job.find_all('p', {'class':'text-sm text-gray-900'})[0].text
				link = url + job.find('a').get('href')
				role = job.find('p', {'class':'text-base font-medium text-brand-600 md:text-sm'}).text
				location = job.find_all('p', {'class':'text-sm text-gray-900'})[1].text
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			except:
				pass
	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()


