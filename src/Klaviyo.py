import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Klaviyo'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# close cookies tab
	# see open positions
	# wait for job listings
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="js-cookie-reject"]'))).click()
	except:
		pass

	view_jobs = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                                       (By.LINK_TEXT, 'View all jobs'))).get_attribute('href')
	driver.get(view_jobs)

	job_list = []

	while True:

		job_cards = driver.find_elements(By.CLASS_NAME, 'card')

		if len(job_cards) != 0:
			for i in range(1, len(job_cards) + 1):
				link = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div[' 
						                   + str(i) + ']/div/h2/a').get_attribute('href')
				role = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
					                       + str(i) + ']/div/h2').text 
				location = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
					                           + str(i) + ']/div/ul/li[1]').text
				team = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
					                       + str(i) + ']/div/ul/li[2]').text
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})

			try:
				next_page = driver.find_element(By.LINK_TEXT, 'Next').get_attribute('href')
				driver.get(next_page)
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
