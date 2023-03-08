import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Intercom'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((
			By.XPATH, '//*[@id="intercom-cookie-consent-banner-wrap"]/div/div/div/span[2]/button'))).click()
	except:
		pass

	# Wait
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jobs"]/div[2]')))

	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('div', {'class':'greenhouse-listings__category'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			team = job.find('span', {'class':'jsx-555748031'}).text
			link = [item.get('href') for item in job.find_all('a', {'class':'greenhouse-listings__job-title-link'})]
			role = [item.text for item in job.find_all('span', {'class':'jsx-2438941253'})]
			location = [item.text for item in job.find_all('span', {'class':'jsx-971543362'})]
			company = company_name

			job_list.append({'Company': company,
							 'Role': role,
							 'Team': team,
							 'Location': location,
							 'Job_URL': link})
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list,
			         columns = columns).explode(['Role', 'Location', 'Job_URL']).reset_index(drop = True)
	
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
