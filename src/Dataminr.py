import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Dataminr'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))).click()
	except:
		pass

	# Open roles
	click_path = '//*[@id="hs_cos_wrapper_widget_1615472200758"]/section/div/div[2]/a[1]'
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_path))).click()

	# Load more
	while True:
		try:
			time.sleep(1)
			load_more = '//*[@id="career-opportunities"]/div[2]/button'
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, load_more))).click()
		except:
			break

	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('div', {'class':'u3m-filtered-content__container'})
	jobs = job_table.find_all('div', {'class':'all'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			link = job.find('a').get('href')
			role = job.find('h3').text.split('\n')[2].strip()
			team = job.find('p').text.split('\n')[2].strip()
			location = job.find_all('p')[1].text.split('\n')[2].strip()
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

