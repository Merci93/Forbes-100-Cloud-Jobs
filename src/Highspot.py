import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Highspot'
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
			                           (By.XPATH, '//*[@id="cookiebanner"]/div[2]/a[1]'))).click()
	except:
		pass

	# Open roles
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
									(By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/div/a'))).click()

	# Open all positions
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-finder-group__heading')))
	groups = driver.find_elements(By.CLASS_NAME, 'job-finder-group')

	for i in range(1, len(groups) + 1):
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="job-finder"]/div[2]/ul/li['
																		+ str(i) + ']'))).click()
		except:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="job-finder"]/div[2]/ul/li['
																			+ str(i) + ']/h4'))).click()
			except:
				pass

	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('li', {'class':'job-finder-group--active'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			team = job.find('h4').text.split('(')[0]
			link = [item.get('href') for item in job.find_all('a')]
			role = [item.text for item in job.find_all('span')][0::2]
			location = [item.text for item in job.find_all('span')][1::2]
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


