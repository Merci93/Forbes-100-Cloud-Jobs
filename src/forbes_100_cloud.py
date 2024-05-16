if __name__ == '__main__':
    import re
    import time
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup as bs

    url = 'https://www.forbes.com/lists/cloud100'

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="truste-consent-button"]').click()

    forbes_100_list = []

    while True:
        time.sleep(1)
        ranks = driver.find_elements(By.CLASS_NAME, 'rank')
        organizations = driver.find_elements(By.CLASS_NAME, 'organizationName')

        forbes_100_list.append({'rank': [rank.text for rank in ranks[:50]],
                                'name': [organization.text.split('.')[0] for organization in organizations[:50]]})
        try:
            if driver.find_element(By.XPATH, '//*[@id="table"]/div[2]/div[3]/div').get_attribute('style') == 'opacity: 1;':
                driver.find_element(By.CLASS_NAME, 'next-button').click()
            else:
                break
        except:
            break

    driver.close()
    forbes_100 = pd.DataFrame(forbes_100_list, columns = ['name', 'rank']).explode(['name', 'rank']).reset_index(drop = True)
    forbes_100['careers_url'] = 'https://www.' + forbes_100['name'].replace(' ', '', regex = True) + '.com/careers'
    forbes_100.to_csv('Scripts/Forbes_100_cloud.csv', index = False)