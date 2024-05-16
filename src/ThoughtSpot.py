import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'ThoughtSpot'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	click_path = '//*[@id="basicPage"]/div/div[1]/section[1]/div/div/div/div/form/input'
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_path))).click()

	# Wait
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'careers_listing_listing__5abZ4')))

	search_body = bs(driver.page_source, 'html.parser')
	departments = search_body.find_all('div', {'class':'careers_listing_listing__5abZ4'})

	job_list = []
	url = 'https://www.thoughtspot.com'

	if len(departments) != 0:
		for job in departments:
			try:
				team = job.find('h3').text
				link = [(url + item.get('href')) for item in job.find_all('a')]
				role = [item.text for item in job.find_all('a')]
				location = [item.text for item in job.find_all('div')][2::3]
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