import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Notion'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	try:
		button_path = '//*[@id="__next"]/div/section/div/section/nav/div[1]/div[2]/button'
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, button_path))).click()
	except:
		pass

	# wait for jobs to load
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.XPATH, '//*[@id="open-positions"]/div[1]/h3')))

	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('section', {'id':'open-positions'})
	categories = search_body.find_all('div', {'class':'jsx-2351126785 title-wrap'})
	jobs = job_table.find_all('ul', {'class':'jsx-2351126785 jobs-list'})

	job_list = []

	if len(jobs) != 0:
		for i in range(0, len(jobs)):
			team = categories[i].text
			link = [item.get('href') for item in jobs[i].find_all('a')]
			role = [item.text for item in jobs[i].find_all('p', {'class':'jsx-2351126785 job-title'})]
			location = [item.text for item in jobs[i].find_all('p', {'class':'jsx-2351126785 job-location'})]
			company = company_name

			job_list.append({'Company': company,
							 'Role': role,
							 'Team': team,
							 'Location': location,
							 'Job_URL': link})
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list,
			          columns = columns).explode(['Role', 'Location', 'Job_URL']).reset_index(drop = True)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()