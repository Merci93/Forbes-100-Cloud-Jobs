import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Rapyd'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
			                           (By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
	except:
		pass

	# Wait for positions to load
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-position-details__list')))
	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('div', {'class':'entry-details'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			link = job.find('a').get('href')
			location = job.find('div', {'class':'name'}).text
			role = job.find_all('li')[0].text
			team = job.find_all('li')[1].text
			company = company_name

			job_list.append({'Company': company,
							 'Role': role,
							 'Team': team,
							 'Location': location,
							 'Job_URL': link})
	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
    