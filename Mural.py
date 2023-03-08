import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Mural'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	pos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
									(By.XPATH, '//*[@id="open-positions"]/div[2]/div/div[3]/div/a'))).get_attribute('href')
	driver.get(pos)

	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('section', {'class':'level-0'})

	job_list = []
	url = 'https://boards.greenhouse.io'

	if len(jobs) != 0:
		for job in jobs:
			try:
				team = job.find('h3').text
				link = [(url + item.get('href')) for item in job.find_all('a')]
				role = [item.text for item in job.find_all('a')]
				location = [item.text for item in job.find_all('span', {'class':'location'})]
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
	df = pd.DataFrame(job_list,
			         columns = columns).explode(['Role', 'Location', 'Job_URL']).reset_index(drop = True)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
