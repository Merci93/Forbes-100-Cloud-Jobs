import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
    company_name = 'Databricks'
    forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
    company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options = options)
    driver.get(company_url)
    driver.maximize_window()

    # Wait
    time.sleep(2)

    search_body = bs(driver.page_source, 'html.parser')
    departments = search_body.find_all('h2', {'class':'my-3'})
    jobs = search_body.find_all('div', {'class':'border-gray-lines border'})
    
    job_list = []
    url = 'https://www.databricks.com'

    if len(jobs) != 0:
        for i in range(0, len(jobs)):
            team = departments[i].text
            role = [item.text for item in jobs[i].find_all('span')][0::2]
            location = [item.text for item in jobs[i].find_all('span')][1::2]
            link = [(url + item.get('href')) for item in jobs[i].find_all('a')]
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
