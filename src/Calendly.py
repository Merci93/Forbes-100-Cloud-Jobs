import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Calendly'
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
			                           (By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
	except:
		pass

	# view all jobs
	# Wait for job table to load
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.XPATH, '//*[@id="job-search"]/div/div[3]/button'))).click()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.XPATH, '//*[@id="content"]/main/div/section/div[2]')))

	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('div', {'class':'card card-job'})

	job_list = []

	if len(jobs) != 0:
		for i in range(1, len(jobs)):
			try:
				role = driver.find_element(By.XPATH, '//*[@id="content"]/main/div/section/div[2]/div['
											+ str(i) + ']/div/h2/a').text
				link = driver.find_element(By.XPATH, '//*[@id="content"]/main/div/section/div[2]/div['
											+ str(i) + ']/div/h2/a').get_attribute('href')
				location = driver.find_element(By.XPATH, '//*[@id="content"]/main/div/section/div[2]/div['
					                           + str(i) + ']/div/ul/li[1]').text
				team = driver.find_element(By.XPATH, '//*[@id="content"]/main/div/section/div[2]/div['
					                       + str(i) + ']/div/ul/li[2]').text
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
    