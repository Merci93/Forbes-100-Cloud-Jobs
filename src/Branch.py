import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Branch'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	click_path = '//*[@id="__next"]/div/main/div/section[1]/div/div[1]/a[1]/button'
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_path))).click()

	# Wait
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tr-group')))

	search_body = bs(driver.page_source, 'lxml')
	jobs = search_body.find_all('div', {'class':'rt-tr-group'})

	job_list = []
	url = 'https://branch.pinpointhq.com'

	if len(jobs) != 0:
		for job in jobs:
			try:
				link = url + job.find('a').get('href')
				role = job.find('a').text.strip()
				team = job.find('div', {'class':'rt-td hide-sm-block col-flex-grow-4'}).text
				location = job.find('div', {'class':'rt-td hide-sm-block col-flex-grow-2'}).text
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

