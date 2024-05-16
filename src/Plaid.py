import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Plaid'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		click_path = '//*[@id="__next"]/div/div[3]/div/div/div/div[3]/div/div[2]/div/button/span/span'
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, click_path))).click()
	except:
		pass

	# Search
	search_tab = '//*[@id="jobSearchForm"]/div/div/div[5]/div/button/span/span[1]'
	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_tab))).click()

	# Wait for data to load
	time.sleep(2)
	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('a', {'class':'grid-x'})

	job_list = []
	url = 'https://plaid.com'

	if len(jobs) != 0:
		for job in jobs:
			link = url + job.get('href')
			team = job.get('href').split('/')[3]
			role = job.find('p', {'class':'OpeningsListRow_title__a5C9M'}).text
			location = job.find('span').text
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
