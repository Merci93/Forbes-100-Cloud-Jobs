import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Benchling'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# open positions
	open_positions = driver.find_element(By.LINK_TEXT, 'See open positions').get_attribute('href')
	driver.get(open_positions)

	# load all open positions
	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
									(By.XPATH, '//*[@id="jobListing"]/div/button'))).click()
		except:
			break

	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('li', {'class':'JobListingFeed_item__WJcWO'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			role = job.find('h3').text
			location = job.find('p').text 
			link = 'https://www.benchling.com/careers'
			team = 'N/A'
			company = company_name

			job_list.append({'Company': company,
							 'Role': role,
							 'Team': team,
							 'Location': location,
							 'Job_URL': link})
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list, columns = columns)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()