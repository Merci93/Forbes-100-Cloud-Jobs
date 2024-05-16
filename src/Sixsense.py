import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = '6sense'
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
			                           (By.XPATH, '//*[@id="lanyard_root"]/div/div/div/div/div[3]/button/span'))).click()
	except:
		pass

	search_body = bs(driver.page_source, 'html.parser')
	job_table = search_body.find('div', {'class':'jet-listing-grid jet-listing'})
	jobs = job_table.find_all('div', {'class':'elementor-widget-heading'})

	job_list = []

	if len(jobs) != 0:
		for i in range(1, len(jobs) + 1):
			for j in range(1, len(jobs) + 1):
				try:
					team = driver.find_element(By.XPATH, '//*[@id="sd_job-deps-listing"]/div/div/div/div['
												+ str(i) + ']/div/section/div/div/div/div[1]/div/h3').text
					role = driver.find_element(By.XPATH, '//*[@id="sd_job-deps-listing"]/div/div/div/div['
												+ str(i) + ']/div/section/div/div/div/div[2]/div/div/div/div['
												+ str(j) + ']/div/section/div/div/div/div[1]/div/h4/a').text
					link = driver.find_element(By.XPATH, '//*[@id="sd_job-deps-listing"]/div/div/div/div['
												+ str(i) + ']/div/section/div/div/div/div[2]/div/div/div/div['
												+ str(j) + ']/div/section/div/div/div/div[1]/div/h4/a').get_attribute('href')
					location = driver.find_element(By.XPATH, '//*[@id="sd_job-deps-listing"]/div/div/div/div['
													+ str(i) + ']/div/section/div/div/div/div[2]/div/div/div/div['
													+ str(j) + ']/div/section/div/div/div/div[3]/div/div/span').text
					company = company_name

					job_list.append({'Company': company,
							                 'Role': role,
							                 'Team': team,
							                 'Location': location,
							                 'Job_URL': link})
				except:
					pass
	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
