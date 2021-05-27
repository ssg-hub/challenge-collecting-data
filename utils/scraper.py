from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Data:
    """
    This class stores all the data scraped from the websites and parses it.
    """
    def __init__(self, url: str):
        self.url: str = url

    def parse(self, data: dict) -> None:
        """
        Parses a dict and adds all data as self attributes 

        :param data: Dictionarry containing data
        """
        for key, val in data.items():
            if val == '':
                val = None
            if (key == "id" or key == "visualisationOption" or key == "specificities"):
                pass
            elif (key == "atticExists"):
                setattr(self, "attic", "Yes" if val == "true" else "No")
            elif (key == "basementExists"):
                setattr(self, "basement", "Yes" if val == "true" else "No")
            elif (key == "bedroom"):
                setattr(self, "bedrooms", data[key]["count"])
            elif (key == "building"):
                setattr(self, "condition", data[key]["condition"])
                setattr(self, "constructionYear", data[key]["constructionYear"])
            elif (key == "kitchen"):
                setattr(self, "kitchen_type", data[key]["type"])
            elif (key == "land"):
                setattr(self, "land_surface", data[key]["surface"])
            elif (key == "outdoor"):
                surf = data[key]["garden"]["surface"]
                setattr(self, "garden_surface", surf if surf else 0)
                setattr(self, "terrace", "Yes" if data[key]["terrace"]["exists"] == "true" else "No")
            elif (key == "energy"):
                setattr(self, "heating_type", data[key]["heatingType"])
            elif (key == "parking"):
                indoor = data[key]["parkingSpaceCount"]["indoor"]
                outdoor = data[key]["parkingSpaceCount"]["outdoor"]
                setattr(self, "parking_indoor", indoor if indoor  != '' else 0)
                setattr(self, "parking_outdoor", outdoor if outdoor != '' else 0)
            else:
                setattr(self, key, val)


class ImmoWebScraper:
    """
    """
    def __init__(self):
        self.driver_options = Options()
        self.driver_options.headless = True
        self.driver: webdriver.Firefox = webdriver.Firefox(executable_path='../../geckodriver/geckodriver.exe', options=self.driver_options)
        self.data_list: List[Data] = []

    def __del__(self):
        self.driver.quit()

    def get_urls(self) -> None:
        """
        Cycle through all the search pages of immoweb, saving all the announcements found in a Data structure
        """
        # Cycle through every page in the search engine
        for i in range(1, 100):
            _URL = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&orderBy=relevance&page={i}"
            self.driver.get(_URL) #url de recherche
            assert "Immoweb" in self.driver.title
            # Search for every announcement links (30 par search page)
            for elem in self.driver.find_elements_by_xpath("//a[@class='card__title-link']"):
                self.data_list.append(Data(elem.get_attribute("href")))

    def scrap_data(self) -> None:
        """
        Executes js script in the web page (returning window.dataLayer object), then adds it to dataFrame
        Maybe will need some webscraping with bs4, if data is incomplete

        For performance, maybe rewrite with http requests, avoids rendering pages ten thousand times 
        """

        for data in self.data_list:
            self.driver.get(data.url)
            
            try:
                raw: dict = self.driver.execute_script("return window.dataLayer")[0].get('classified')
                data.parse(raw)
                # data[1] info about the seller
            except:
                data = None
            if not data:
                print("---\nData is none\n---")


    def fill_dataframe(self) -> None:
        """
        Converts all the objects present in self.data_list to disctionaries, then feed them to the dataframe.
        """
        self.df: DataFrame = pd.DataFrame([data.__dict__ for data in self.data_list])