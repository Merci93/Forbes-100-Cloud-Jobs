import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Attentive'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	open_roles = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
		                                       (By.LINK_TEXT, 'See Open Roles'))).get_attribute('href')
	driver.get(open_roles)

	# wait for page to load
	# get page source
	# get role tables
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lever-team')))
	search_body = bs(driver.page_source, 'lxml')
	role_tables = search_body.find_all('ul', {'class': 'lever-team'})

	job_list = []

	if len(role_tables) != 0:
		for table in role_tables:
			try:
				team = table.find('div', {'class':'lever-team-title'}).text
				location = [item.text for item in table.find_all('span', {'class':'lever-job-tag'})]
				link = [item.get('href') for item in table.find_all('a', {'class':'lever-job-title'})]
				role = [item.text for item in table.find_all('a', {'class':'lever-job-title'})]
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
	df = pd.DataFrame(job_list,
			         columns = columns).explode(['Role', 'Location', 'Job_URL']).reset_index(drop = True)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
