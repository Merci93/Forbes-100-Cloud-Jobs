import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
    company_name = 'Canva'
    forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
    company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options = options)
    driver.get(company_url)
    driver.maximize_window()

    last_height = driver.execute_script('return document.body.scrollHeight')

    # scroll to through page to load data
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    view_all_jobs = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                                  (By.XPATH, '//*[@id="js-home-main"]/div'
                                                   + '/section[5]/div[1]/div/div[2]'
                                                   + '/a'))).get_attribute('href')
    driver.get(view_all_jobs)

    # accept essential cookies
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                  (By.XPATH, '//*[@id="js-cookie-reject"]'))).click()

    job_list = []

    while True:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
        job_cards = driver.find_elements(By.CLASS_NAME, 'card')
        
        if len(job_cards) != 0:
            for i in range(1, len(job_cards) + 1):
                role = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div[' 
                                           + str(i) + ']/div/h2').text
                link = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
                                           + str(i) + ']/div/h2/a').get_attribute('href')
                team = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
                                           + str(i) + ']/div/ul/li[1]').text
                location = driver.find_element(By.XPATH, '//*[@id="js-job-search-results"]/div['
                                               + str(i) + ']/div/ul/li[2]').text
                company = company_name    

                job_list.append({'Company': company,
                                 'Role': role,
                                 'Team': team,
                                 'Location': location,
                                 'Job_URL': link})
            try:
                next_page = driver.find_element(By.LINK_TEXT, 'Next').get_attribute('href')
                driver.get(next_page)
            except:
                break
        else:
            print(company_name + ': No data obtained')
            break
        
    df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
    df.drop_duplicates(inplace = True)
    df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
    