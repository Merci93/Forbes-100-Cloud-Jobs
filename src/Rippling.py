import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Rippling'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	pos_path = '//*[@id="__next"]/div/main/div[1]/div/div/div[1]/a'
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pos_path))).click()

	time.sleep(2)
	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('div', {'class':'grid'})
	jobs = job_table.find_all('div', {'class':'group'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			link = job.find('a').get('href')
			role = job.find_all('p')[0].text.strip()
			team = job.find_all('p')[1].text
			location = job.find_all('div')[1].text.strip()
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

    