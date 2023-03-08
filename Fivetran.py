import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Fivetran'
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

	search_body = bs(driver.page_source, 'html.parser')
	job_table = search_body.find_all('div', {'class':'w-layout-grid jobs__department'})
	jobs = [item.find_all('div', {'class':'vertical__16'}) for item in job_table]

	job_list = []

	if len(jobs) != 0:
		for i in range(0, len(jobs)):
			for j in range(0, len(jobs[i])):
				team = job_table[i].find('div', {'class':'text__eyebrow text__gradient-purple'}).text
				role = jobs[i][j].find('div', {'class':'text__subhead'}).text
				link = jobs[i][j].find('a').get('href')
				location = jobs[i][j].find('a').text
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
    