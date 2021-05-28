from selenium import webdriver
from utils.utils import websc
import time

websc = websc()
driver = webdriver.Chrome("/usr/bin/chromedriver")

for i in range(1, 333):
    websc.change_my_page(i)
    print(f"\n\n !!! \n\n NEW PAGE ==> {websc.search_url}\n  PAGE NUMBER ==> {websc.page_number}\n\n\n !!! \n\n ")
    driver.get(websc.search_url)
    time.sleep(1)
    print (websc.search_url)
    assert "Immoweb" in driver.title
    for elem in driver.find_elements_by_xpath("//a[@class='card__title-link']"): #liens des maisons
        websc.properties_url.append(elem.get_attribute("href"))
        websc.simple_property_URL = elem.get_attribute("href")
        timecount= time.perf_counter()
        print(f'\n  NEW_URL_PROPERTY ==> {websc.simple_property_URL}\n  PROPERTY NUMBER ==> {websc.property_nbr} / {websc.total_property_number}     Time : {timecount - websc.timeStart:f} seconds\n  PAGE NUMBER ==> {websc.page_number} / {websc.total_page_number}\n')
        websc.property_nbr += 1
websc.property_nbr = 1

for url in websc.properties_url:
    timecount = time.perf_counter()
    driver.get(url)
    time.sleep(1)
    websc.data = driver.execute_script("return window.dataLayer")
    print(f'\n  PROPERTY_SCRAP ==> {url}\n  PROPERTY NUMBER ==> {websc.property_nbr} / {websc.total_property_number}    Time : {timecount - websc.timeStart:f} seconds\n  PAGE NUMBER ==> {round (websc.property_nbr / 30)} / {websc.total_page_number}\n')
    websc.property_nbr += 1
    websc.crawl()


websc.create_csv()
driver.close()

print("\n\n§§§§§DONE§§§§§")