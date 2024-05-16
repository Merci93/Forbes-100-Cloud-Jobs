import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Talkdesk'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Page scroll
	driver.execute_script('window.scrollTo(0, 900)')

	# Open positions
	open_path = '/html/body/div[2]/div[2]/section[5]/div/div/div/div[2]/div/div[1]/div[1]'
	WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, open_path)))
	search_body = bs(driver.page_source, 'lxml')
	job_dept = search_body.find_all('div', {'class':'au-target col-md-4 content-list-item'})

	job_list = []

	if len(job_dept) != 0:
		for i in range(1, len(job_dept) + 1):
			driver.execute_script('window.scrollTo(0, 900)')
			wait_path = '/html/body/div[2]/div[2]/section[5]/div/div/div/div[2]/div/div[1]/div[' + str(i) + ']'
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, wait_path)))
			driver.find_element(By.XPATH, wait_path).click()

			time.sleep(2)
			search_body = bs(driver.page_source, 'lxml')
			jobs = search_body.find_all('div', {'class':'job-title'})

			for i in range(1, len(jobs) + 1):
				time.sleep(1)
				try:
					role = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]/'
												+ 'section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
												+ ']/div[1]/div[1]/span/a/div/span').text
				except:
					try:
						time.sleep(2)
						role = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]/'
													+ 'section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
													+ ']/div[1]/div[1]/span/a/div/span').text
					except:
						continue
				try:
					link = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]/'
												+ 'section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
												+ ']/div[1]/div[1]/span/a').get_attribute('href')
				except:
					try:
						time.sleep(2)
						link = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]/'
													+ 'section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
													+ ']/div[1]/div[1]/span/a').get_attribute('href')
					except:
						continue
				try:
					location = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]'
													+ '/section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
													+ ']/div[1]/div[1]/p[1]/span[1]/span').text.split('\n')[1]
				except:
					try:
						time.sleep(2)
						location = driver.find_element(By.XPATH, '//*[@id="acc-skip-content"]/div[2]/div/div/div/div[2]'
														+ '/section[1]/div/div/div/div[1]/div[2]/div[2]/ul/li[' + str(i)
														+ ']/div[1]/div[1]/p[1]/span[1]/span').text.split('\n')[1]
					except:
						continue
				team = search_body.find('span', {'class':'facet-tag'}).text
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			# Return to previous page
			driver.back()

	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
