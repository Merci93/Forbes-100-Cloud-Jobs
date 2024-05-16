import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = '1Password'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	pos = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
										  (By.XPATH, '/html/body/main/section[2]/div/div/a'))).get_attribute('href')
	driver.get(pos)

	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('div', {'class':'postings-group'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			try:
				link = link = [item.get('href') for item in job.find_all('a', {'class':'posting-title'})]
				location = [item.text for item in job.find_all('span', {'class':'location'})]
				role = [item.text for item in job.find_all('h5')]
				team = [item.text.replace(' – ', ' ') for item in job.find_all('span', {'class':'department'})]
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
			         columns = columns).explode(['Team', 'Role', 'Location', 'Job_URL']).reset_index(drop = True)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()