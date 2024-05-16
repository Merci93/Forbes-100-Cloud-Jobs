import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Webflow'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open roles
	click_path = '//*[@id="main"]/header/section[1]/div[1]/div[2]/div/a'
	pos = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
									(By.XPATH, click_path))).get_attribute('href')
	driver.get(pos)

	time.sleep(2)
	search_body = bs(driver.page_source, 'html.parser')
	job_table = search_body.find('div', {'id':'jobs-list'})
	jobs = job_table.find_all('section')

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			team = job.find('h2').text
			role = [item.text for item in job.find_all('h3')]
			location = [item.text for item in job.find_all('div', {'class':'jobs-listing_location'})]
			link = [item.get('href') for item in job.find_all('a')]
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
