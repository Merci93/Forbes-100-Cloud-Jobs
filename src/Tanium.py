import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Tanium'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))).click()
	except:
		pass

	# Wait
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item')))

	job_categories = driver.find_elements(By.CLASS_NAME, 'item')

	job_list = []

	if len(job_categories) != 0:
		for i in range(1, len(job_categories) + 1):
			driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div/div/div['
				                + str(i) + ']').click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-row')))

			jobs = driver.find_elements(By.CLASS_NAME, 'job-row')
			
			for j in range(2, len(jobs) + 1):
				team = driver.find_element(By.XPATH, '//*[@id="jobs"]/h3').text
				link = driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div/div/div/a['
					                       + str(j) + ']').get_attribute('href')
				role = driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div/div/div/a['
					                       + str(j) + ']/h4[1]').text
				location = driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div/div/div/a['
											   + str(j) + ']/h4[2]').text
				company = company_name

				job_list.append({'Company': company,
			                 	 'Role': role,
			                 	 'Team': team,
			                 	 'Location': location,
			                 	 'Job_URL': link})

			driver.back()
	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
