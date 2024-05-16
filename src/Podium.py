import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Podium'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Openings
	driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/main/div[1]/div/div/div[1]/div[2]/div/a').click()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/section[1]')))

	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('section', {'class':'level-0'})

	job_list = []
	url = 'https://boards.greenhouse.io'

	if len(jobs) != 0:
		for job in jobs:
			team = job.find('a').text
			role = [item.text for item in job.find_all('a')]
			link = [(url + item.get('href')) for item in job.find_all('a')]
			location = [item.text for item in job.find_all('span', {'class':'location'})]
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
