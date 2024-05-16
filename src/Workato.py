import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Workato'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		click_path = '//*[@id="__layout"]/div/div/div/div/div/section/div[1]/div/div/button'
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, click_path))).click()
	except:
		pass

	# Load page data
	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
											(By.XPATH, '//*[@id="jobs"]/div/div[2]/div/div[3]'))).click()
		except:
			break

	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('li', {'class':'job-list__item'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			link = job.find('a').get('href')
			role = job.find('div', {'job-vacancy__title'}).text
			location = job.find('div', {'class':'job-vacancy__location'}).text
			team = 'N/A'
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
    