import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Mambu'
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
			                           (By.XPATH, '//*[@id="hs-eu-decline-button"]'))).click()
	except:
		pass

	# Join us
	positions = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
										  		(By.LINK_TEXT, 'Join us'))).get_attribute('href')
	driver.get(positions)

	# Switch to iframe
	iframe = driver.find_element(By.ID, 'icims_content_iframe')
	driver.switch_to.frame(iframe)

	# Search
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
									(By.XPATH, '//*[@id="jsb_form_submit_i"]'))).click()
	time.sleep(2)
	search_body = bs(driver.page_source, 'html.parser')
	pages = [item.get('href') for item in search_body.find('div', {'class':'iCIMS_PagingBatch'}).find_all('a')]

	job_list = []

	if len(pages) != 0:
		for page in pages:
			driver.get(page)
			iframe = driver.find_element(By.ID, 'icims_content_iframe')
			driver.switch_to.frame(iframe)
			time.sleep(2)
			search_body = bs(driver.page_source, 'html.parser')
			job_table = search_body.find('div', {'class':'container-fluid iCIMS_JobsTable'})
			jobs = job_table.find_all('div', {'class':'row'})

			for job in jobs:
				location = job.find_all('span')[1].text.strip().replace('|', ',')
				link = job.find('a').get('href')
				role = job.find('h2').text.strip()
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