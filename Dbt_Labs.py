import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Dbt Labs'
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
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'job-title')))
	
	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('div', {'class':'jobs-list'})
	jobs = job_table.find_all('div', {'class':'row'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			link = job.find('a', {'class':'job-title'}).get('href')
			role = job.find('a', {'class':'job-title'}).text
			team = job.find('p', {'class':'tags'}).text.split(',')[0]
			location = job.find('p', {'class':'tags'}).text.split(',')[1].strip()
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
