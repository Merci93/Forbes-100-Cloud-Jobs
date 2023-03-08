import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Gong'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# close cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
	except:
		pass

	# Wait
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.CLASS_NAME, 'CurrentOpeningsBlock-results')))

	job_list = []

	while True:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                            (By.CLASS_NAME, 'CurrentOpeningsBlock-results')))
		search_body = bs(driver.page_source, 'lxml')
		job_table = search_body.find('div', {'class':'CurrentOpeningsBlock-results'})
		jobs = job_table.find_all('a')

		if len(jobs) != 0:
			for job in jobs:
				link = 'https://www.gong.io' + job.get('href')
				role = job.find('span', {'class':'CurrentOpeningsBlock-resultTitle'}).text
				team = job.find('span', {'class':'CurrentOpeningsBlock-resultDepartment'}).text
				location = job.find('span', {'class':'CurrentOpeningsBlock-resultLocation'}).text
				company = company_name

				job_list.append({'Company': company,
				             	 'Role': role,
				             	 'Team': team,
				             	 'Location': location,
				             	 'Job_URL': link})
			try:
				driver.find_element(By.CLASS_NAME, 'CurrentOpeningsBlock-next').click()
			except:
				break
		else:
			print(company_name + ': No data obtained')
			break

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
