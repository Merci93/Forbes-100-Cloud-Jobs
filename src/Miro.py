import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Miro'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Open positions
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
									(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/nav/div[2]/a'))).click()
	job_list = []
	url = 'https://miro.com'

	for i in range(1, 101):
		try:
			page = 'https://miro.com/careers/open-positions/?searchTerm=&selectedTeam=&selectedLocation=&currentPage='+str(i)
			driver.get(page)

			# Wait
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
										   (By.XPATH, '//*[@id="jobList"]/div[2]/ul/li[1]/a/div[1]/h4')))
			search_body = bs(driver.page_source, 'lxml')
			job_table = search_body.find('div', {'id':'jobList'})
			jobs = job_table.find_all('a', {'class':'JobListItem_job__ZAsZo'})

			for job in jobs:
				try:
					link = url + job.get('href')
					role = job.find('h4').text
					team = job.find_all('li')[0].text
					location = job.find_all('li')[1].text
					company = company_name

					job_list.append({'Company': company,
					                 'Role': role,
					                 'Team': team,
					                 'Location': location,
					                 'Job_URL': link})
				except:
					continue
		except:
			break
	
	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()

