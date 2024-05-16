import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

# careers_url = 'https://www.Lucid.co/careers'

# def scrape():
# 	company_name = 'Lucid'
# 	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
# 	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
# 	driver = webdriver.Chrome()
# 	driver.get(company_url)

# 	# Close cookies
# 	try:
# 		click_path = '//*[@id="5b4072a2-1217-4054-b26e-a21637bae196"]/div[2]/button[2]'
# 		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_path))).click()
# 	except:
# 		pass

# 	# Open all available roles
# 	time.sleep(2)
# 	expand_button = driver.find_elements(By.CLASS_NAME, 'css-1q3uuzw')

# 	for i in range(1, len(expand_button) + 1):
# 		time.sleep(2)
# 		try:
# 			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
# 											(By.XPATH, '//*[@id="open-positions"]/div[2]/div[2]/div['
# 												+ str(i) + ']/button'))).click()
# 		except:
# 			try:
# 				time.sleep(2)
# 				WebDriverWait(driver, 10).until(EC.presence_of_element_located(
# 												(By.XPATH, '//*[@id="open-positions"]/div[2]/div[2]/div['
# 													+ str(i) + ']'))).click()
# 			except:
# 				time.sleep(2)
# 				try:
# 					WebDriverWait(driver, 10).until(EC.presence_of_element_located(
# 													(By.XPATH, '//*[@id="open-positions"]/div[2]/div[2]/div['
# 														+ str(i) + ']/button'))).click()
# 				except:
# 					try:
# 						time.sleep(2)
# 						WebDriverWait(driver, 10).until(EC.presence_of_element_located(
# 														(By.XPATH, '//*[@id="open-positions"]/div[2]/div[2]/div['
# 															+ str(i) + ']'))).click()
# 					except:
# 						pass

# 	search_body = bs(driver.page_source, 'lxml')
# 	job_table = search_body.find('div', {'class':'css-178yklu e1n7skr50'})
# 	jobs = job_table.find_all('div', {'class':'css-0 e1n7skr50'})[1:]

# 	job_list = []

# 	if len(jobs) != 0:
# 		for job in jobs:
# 			team = job.find('h3').text
# 			role = [item.text for item in job.find_all('div', {'class':'css-rjjx35 e1n7skr50'})]
# 			link = [item.get('href') for item in job.find_all('a')][0::2]
# 			location = [item.text for item in job.find_all('span', {'class':'css-wy3sor-text efcxqvi0'})]
# 			company = company_name

# 			job_list.append({'Company': company,
# 						     'Role': role,
# 						     'Team': team,
# 						     'Location': location,
# 						     'Job_URL': link})
# 	else:
# 		print(company_name + ': No data obtained')

# 	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
# 	df = pd.DataFrame(job_list,
# 			         columns = columns).explode(['Role', 'Location', 'Job_URL']).reset_index(drop = True)

# 	df.drop_duplicates(inplace = True)
# 	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

# if __name__ == '__main__':
#     scrape()

