# ICAO Type Designator Scraper
 A simple Python script to scrape the online ICAO Type Designator page (https://www.icao.int/publications/doc8643/pages/search.aspx).
 
# Why?
Although ICAO publishes the type designator database online, it is not in an exportable-friendly format. So I wrote a short script using Selenium to handle the JS execution and pagination and BeautifulSoup to parse/extract the HTML table context (since it's WAY faster than Selenium for that bit). It outputs all 10,000+ entries into a CSV file.

# How do I run it?
1. Make sure that Selenium and BeautifulSoup are installed in your Python environment or virtual environment.
```
pip install selenium
pip install bs4
```
2. Download ChromeDriver (https://chromedriver.chromium.org/downloads) and place `chromedriver.exe` in the same directory as the Python script. Or you can use a different Selenium webdriver, but that will require knowing how to change it in the script.
3. Run the Python script `aircraftscrape.py`. It will output a CSV file with the timestamp of when the script was run.

# Why not distribute the data?
Because the ICAO terms and conditions says I shouldn't.
