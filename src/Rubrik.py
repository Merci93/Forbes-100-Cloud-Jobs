import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Rubrik'
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
			                           (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
	except:
		pass

	# job rows
	job_categories = driver.find_elements(By.CLASS_NAME, 'careers_departments_grid_item')
	departments = [job_categories[j].text.split('\n')[0] for j in range(0, len(job_categories))]

	job_list = []
	url = 'https://www.rubrik.com'

	if len(departments) != 0:
		for i in range(1, len(job_categories) + 1):
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
				                           (By.CLASS_NAME, 'careers_departments_grid_item')))
			driver.find_element(By.XPATH, '//*[@id="departments"]/div[2]/div/div/div/div[1]/div/div/div['
				                + str(i) + ']/a').click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
				                           (By.CLASS_NAME, 'careers_section_listing_container')))

			search_body = bs(driver.page_source, 'lxml')
			jobs = search_body.find_all('div', {'class':'careers_section_listing_container span-10-d'})

			for job in jobs:
				team = departments[i - 1]
				location = job.find('h4').text
				link = [(url + item.get('href')) for item in job.find_all('a', {'class': 'careers_section_listing_job_item_anchor'})]
				role = [item.text for item in job.find_all('p', {'class':'careers_section_listing_job_item_title'})]
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			driver.back()
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list,
			         columns = columns).explode(['Role', 'Job_URL']).reset_index(drop = True)
	
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
