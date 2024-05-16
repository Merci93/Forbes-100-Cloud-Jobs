import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'ServiceTitan'
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

	# Explore openings (join us)
	pos = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                                 (By.LINK_TEXT, 'Join us'))).get_attribute('href')
	driver.get(pos)

	job_list = []

	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
				                           (By.CLASS_NAME, 'job-listing--card-title')))
			job_box = driver.find_elements(By.CLASS_NAME, 'job-listing--card-title')

			if len(job_box) != 0:
				for i in range(1, len(job_box) + 1):
					role = driver.find_element(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div['
						                       + str(i) + ']/p').text
					location = driver.find_element(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div['
						                           + str(i) + ']/div/div[1]/p').text
					link = driver.find_element(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div['
											   + str(i) + ']/a').get_attribute('href')
					team = 'N/A'
					company = company_name
											  
					job_list.append({'Company': company,
				                     'Role': role,
				                     'Team': team,
				                     'Location': location,
				                     'Job_URL': link})

				# Next page
				try:
					WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
						(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div[9]/ul/li[7]/div'))).click()
				except:
					try:
						WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
							(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div[9]/ul/li[8]/div'))).click()
					except:
						try:
							WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
								(By.XPATH, '//*[@id="job-openings"]/div/div[2]/div[2]/div[9]/ul/li[9]/div'))).click()
						except:
							break
			else:
				print(company_name + ': No data obtained')
				break
		except:
			break

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
    