import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'TripActions'
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

	# Job openings
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
						(By.XPATH, '//*[@id="__next"]/section[1]/div[4]/div[2]/div/div[2]/a/button'))).click()

	# Wait for data to load
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
									(By.XPATH, '//*[@id="__next"]/div[3]/ul/li[3]/div[1]'))).click()

	search_body = bs(driver.page_source, 'html.parser')
	job_table = search_body.find('div', {'class':'container-width pb-10'})
	jobs = job_table.find_all('li')

	job_list = []
	url = 'https://navan.com'

	if len(jobs) != 0:
		for job in jobs[1:]:
			link = url + job.find('a').get('href')
			role = job.find('a').text
			team = job.find('div').text
			location = job.find_all('div')[1].text
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
