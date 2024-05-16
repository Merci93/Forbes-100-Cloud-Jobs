import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Scale AI'
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

	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="positions"]/ul')))
	search_body = bs(driver.page_source, 'html.parser')
	class_tag = 'class="px-8 py-8 transition-shadow duration-300 ease-out rounded-lg shadow-md hover:shadow-xl"'
	jobs = re.findall(class_tag, str(search_body))

	job_list = []

	if len(jobs) != 0:
		for i in range(1, len(jobs) + 1):
			link = driver.find_element(By.XPATH, '//*[@id="positions"]/ul/li[' + str(i) + ']/a').get_attribute('href')
			role = driver.find_element(By.XPATH, '//*[@id="positions"]/ul/li[' + str(i) + ']/a/h3').text
			location = driver.find_element(By.XPATH, '//*[@id="positions"]/ul/li[' + str(i) + ']/a/div[1]').text
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
