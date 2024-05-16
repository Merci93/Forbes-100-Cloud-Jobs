import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Automattic'
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
			                           (By.XPATH, '/html/body/div[4]/a'))).click()
	except:
		pass

	# Load page data
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
									(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div')))

	search_body = bs(driver.page_source, 'lxml')
	position_table = search_body.find_all('div', {'class':'wp-block-group__inner-container'})
	jobs = position_table[2].find_all('li')

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			try:
				team = job.find('a').text
				link = job.find('a').get('href')
				role = 'N/A'
				location = 'N/A'
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

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()

