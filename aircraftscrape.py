from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
import csv
from bs4 import BeautifulSoup
from datetime import datetime

CHROMEDRIVER_PATH = 'chromedriver.exe'
ICAO_SITE = 'https://www.icao.int/publications/doc8643/pages/search.aspx'

def scrape(output_filename=None):

    # Hardcoded options for now
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Create driver and wait a little to load JS. Should use the proper Selenium visibility test fuctions, 
    # but hacking is faster
    driver.get(ICAO_SITE)
    time.sleep(10)

    # We will open the csv output file now because we write as we go
    # TODO -- should be smarter about the name here, could get the "Last Updated" date from page
    if output_filename is None:
        output_filename = datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:

        # Setup CSV writer and start with header
        fieldnames = [
            'Type Designator',
            'Manufacturer',
            'Model',
            'Description',
            'Engine Type',
            'Engine Count',
            'WTC'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        # Select the dropdown for 100 entries to make fewer calls
        select = Select(driver.find_element(By.ID, 'atd-table_length').find_element(By.TAG_NAME, 'select'))
        select.select_by_visible_text('100')

        # Loop over all of the table pages
        loop = True
        while(loop):
            
            # Getting the current page's table HTML and bring into BeautifulSoup for WAY faster parsing
            tableHTML = driver.find_element(By.CSS_SELECTOR, '#atd-table-body').get_attribute('innerHTML')
            soup = BeautifulSoup(tableHTML, 'html.parser')
            
            # Iterate over each table row and create the type designator dict for CSV writing
            rows = soup.find_all('tr')
            page_results = []
            for row in rows:
                cell_texts = [cell.text.strip() for cell in row.find_all('td')]
                result_dict = {
                    'Type Designator' : cell_texts[2],
                    'Manufacturer'    : cell_texts[0],
                    'Model'           : cell_texts[1],
                    'Description'     : cell_texts[3],
                    'Engine Type'     : cell_texts[4],
                    'Engine Count'    : cell_texts[5],
                    'WTC'             : cell_texts[6]
                }
                page_results.append(result_dict)

            # Write once per page after going through all the rows
            writer.writerows(page_results)

            # Get the next pagination link
            pagination_row = driver.find_element(By.CSS_SELECTOR, '#atd-table_paginate')
            next_box = pagination_row.find_element(By.CSS_SELECTOR, '#atd-table_next')

            # Check if we are on the last page. If not, click on next page link and continue
            if 'disabled' in next_box.get_attribute('class'):
                loop = False
            else:
                next_link = next_box.find_element(By.TAG_NAME, 'a')
                next_link.click()

if __name__ == '__main__':
    scrape()