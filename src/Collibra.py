import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Collibra'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.XPATH, '//*[@id="cookiescript_accept"]'))).click()
	# Open all available roles
	expand_button = driver.find_elements(By.CLASS_NAME, 'cmp-joblist__department')

	for i in range(0, len(expand_button)):
		time.sleep(2)
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="constrict_expand-'
																			+ str(i) + '"]/button'))).click()
		except:
			try:
				time.sleep(1)
				driver.find_element(By.XPATH, '//*[@id="jobs-filter"]/span/button[' + str(i + 1) + ']').click()
			except:
				try:
					time.sleep(1)
					driver.find_element(By.XPATH, '//*[@id="constrict_expand-' + str(i) + '"]/div').click()
				except:
					try:
						time.sleep(1)
						driver.find_element(By.XPATH, '//*[@id="jobs-filter"]/span/button[' + str(i + 1) + ']').click()
					except:
						pass

	search_body = bs(driver.page_source, 'lxml')
	job_filter = search_body.find('div', {'id':'jobs-filter'})
	job_dept = job_filter.find_all('button', {'class':'cmp-joblist__department active'})
	jobs = job_filter.find_all('div', {'class':'cmp-joblist__detail'})

	job_list = []
	url = 'https://www.collibra.com/'

	if len(jobs) != 0:
		for i in range(1, len(job_dept) + 1):
			job_item = jobs[i - 1].find_all('h4')

			for j in range(1, len(job_item) + 2):
				try:
					team = job_dept[i - 1].find('h3').text
					role = driver.find_element(By.XPATH, '//*[@id="jobs-filter"]/span/div[' + str(i)
												+ ']/div[' + str(j) + ']/h4').text
					link = driver.find_element(By.XPATH, '//*[@id="jobs-filter"]/span/div[' + str(i)
												+ ']/div[' + str(j) + ']/ul/li[1]/a').get_attribute('href')
					location = driver.find_element(By.XPATH, '//*[@id="jobs-filter"]/span/div[' + str(i)
													+ ']/div[' + str(j) + ']/ul/li[1]/a/div/span').text.split(' in ')[1]
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
	df = pd.DataFrame(job_list, columns = columns)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()


