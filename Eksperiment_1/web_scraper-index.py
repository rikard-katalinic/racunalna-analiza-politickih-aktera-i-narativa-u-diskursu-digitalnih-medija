from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from bs4 import BeautifulSoup
import pandas as pd
import requests, time
from datetime import datetime

article_tags = [
    'https://www.index.hr/tag/86/hdz.aspx',
    'https://www.index.hr/tag/256/sdp.aspx',
    'https://www.index.hr/tag/1020361/mozemo.aspx',
    'https://www.index.hr/tag/3724/most.aspx',
    'https://www.index.hr/tag/101/vlada.aspx',
    'https://www.index.hr/tag/4482/hrvatski-sabor.aspx',
    'https://www.index.hr/tag/20416/andrej-plenkovic.aspx',
    'https://www.index.hr/tag/93294/zoran-milanovic.aspx',
    'https://www.index.hr/tag/1001140/gordan-jandrokovic.aspx'
]
data = []

print("Dohvaćanje URL-ova...")
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)
for i, url in enumerate(article_tags):
    driver.get(url)

    if i == 0:
        wait = WebDriverWait(driver, 5)
        buttons_div = wait.until(EC.presence_of_element_located((By.ID, 'buttons')))
        buttons = buttons_div.find_elements(By.TAG_NAME, 'button')
        buttons[1].click()

    while True:
        dates = driver.find_elements(By.XPATH, '/div[@class="publish-date"]')
        year = int(dates[-1].text.split('.')[-2])
        if year < 2025:
            break

        wait = WebDriverWait(driver, 5)
        load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'read-more-text')))

        ActionChains(driver).move_to_element(load_more_button).perform()
        load_more_button.click()
            
        time.sleep(1)


    link_elements = driver.find_elements(By.XPATH, '/div[@class="articles-container"]//a')
    dates = driver.find_elements(By.XPATH, '/div[@class="publish-date"]')

    print("\nWeb scraping ", url, ":", sep="")
    for link, dates in zip(link_elements, dates):
        year = int(dates.text.split('.')[-2])
        if year == 2026:
            continue
        if year == 2024:
            break

        url = link.get_attribute('href')
        response = requests.get(url)
        date_object = datetime.strptime(dates.text, '%d.%m.%Y.')

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1', class_='js-main-title')
            if title is not None:
                title = title.text.strip()
                
            content_paragraphs = ''
            paragraphs = soup.select('section.text p')
            for p in paragraphs:
                if p:
                    content_paragraphs += ' ' + p.get_text(strip=True)
            
            content_tags = ''
            tags = soup.select('nav.tags-holder a')
            for t in tags:
                if t:
                    content_tags += t.get_text(strip=True)[1:] + ','

            data.append([date_object, url, 'Index.hr', title, content_paragraphs, content_tags[:-1]])
driver.quit()


df = pd.DataFrame(
    data, columns=['date_published', 'link', 'publisher', 'title', 'content', 'tags']
).drop_duplicates()
df.to_excel('articles_index.xlsx')
print("\nPodaci spremljeni!")
