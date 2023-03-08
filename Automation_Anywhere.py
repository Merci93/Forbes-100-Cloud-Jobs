import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Automation Anywhere'
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
			                           (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
	except:
		pass

	# Wait for job frame
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jv_careersite_iframe_id"]')))

	# Switch to iframe
	driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find_all('table', {'class':'jv-job-list'})

	job_list = []
	url = 'https://jobs.jobvite.com'

	if len(job_table) != 0:
		for i in range(0, len(job_table)):
			try:
				team = search_body.find_all('h3')[i].text 
				role = [item.text.replace('\n', '') for item in job_table[i].find_all('td', {'class':'jv-job-list-name'})]
				link = [(url + item.get('href')) for item in job_table[i].find_all('a')]
				location = [item.text.replace('\n','').strip() for item in job_table[i].find_all('td', {'class':'jv-job-list-location'})]
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




