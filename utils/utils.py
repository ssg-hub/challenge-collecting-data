import random
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import json
import jmespath as jp
from typing import List, Dict, Tuple
import csv

class websc:

    locality : List[str] = []
    type_of_property : List[str]= []
    subtype_of_property : List[str] = []
    price : List[float] = []
    type_of_sale : List[str] = []
    number_of_rooms : List[int] = []
    area_in_sq_meters : List[float] = []
    fully_equipped_kitchen : List[bool] = []
    furnished : List[bool] = []
    open_fire : List[bool] = []
    terrace : List[bool] = []
    terrace_area : List[float] = []
    garden : List[bool] = []
    garden_area : List[float] = []
    surface_of_the_land : List[float] = []
    number_of_facades : List[int] = []
    swimming_pool : List[bool] = []
    state_of_the_building : List [str] = []
    df_list : list = []
    page_number : int = 1
    search_url : str = []
    simple_property_URL : str = []
    properties_url : List[str] = []
    data : list = []
    temp_dict : dict = {}
    df = list
    my_df = pd.DataFrame()
    timeStart = time.perf_counter()
    property_nbr = 0
    total_page_number = 333
    total_property_number = 14769
    
    def change_my_page(self, nbr: int) -> None: #Function that generate new URL to go page to page
        self.page_number = nbr
        self.search_url = (f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&propertySubtypes=BUNGALOW,CASTLE,COUNTRY_COTTAGE,TOWN_HOUSE,VILLA,MANOR_HOUSE,GROUND_FLOOR,TRIPLEX,PENTHOUSE,CHALET,FARMHOUSE,EXCEPTIONAL_PROPERTY,MANSION,PAVILION,DUPLEX,FLAT_STUDIO,LOFT,APARTMENT_BLOCK&page={nbr}&orderBy=relevance")

    def crawl(self) -> None: #
        for i in self.data:
            for k,v  in enumerate(i):
                if v == 'classified':
                    self.temp_dict = list(i.items())[k][1]
                    self.parse_data()
                    
    def parse_data(self) -> None: #Parse data from dictionnary
    
        try:
            zip_code = jp.search('zip', self.temp_dict)
        except IndexError:
            zip_code = None
        self.locality.append(zip_code)
        
        try:
            type_property = jp.search('type', self.temp_dict)
        except IndexError:
            type_property = None
        self.type_of_property.append(type_property)

        try:
            subtype_property = jp.search('subtype', self.temp_dict)
        except IndexError:
            subtype_property = None
        self.subtype_of_property.append(subtype_property)
        
        try:
            price_property = jp.search('price', self.temp_dict)
        except IndexError:
            price_property = None
        self.price.append(price_property)

        try:
            type_sale = jp.search('transactionType', self.temp_dict)
        except IndexError:
            type_sale = None
        self.type_of_sale.append(type_sale)
        
        try:
            rooms = jp.search('bedroom.count', self.temp_dict)          
        except IndexError:
            rooms = None
        self.number_of_rooms.append(rooms)

        try:
            area = jp.search('land.surface', self.temp_dict)
        except IndexError:
            area = None
        self.area_in_sq_meters.append(area)

        try:
            kitchen = jp.search('kitchen.type', self.temp_dict)
            kitchen = True
        except IndexError:
            kitchen = False
        self.fully_equipped_kitchen.append(kitchen)

        try:
            trc = jp.search('outdoor.terrace.exists', self.temp_dict)
            if trc == 'true': trc = True
        except IndexError:
            trc = False
        self.terrace.append(trc)

        try:
            grdn = jp.search('outdoor.garden.exists', self.temp_dict)
            if grdn == 'true': grdn = True
        except IndexError:
            grdn = False
        self.garden.append(grdn)
         
        try:
            swim_pool= jp.search('wellnessEquipment.hasSwimmingPool.type', self.temp_dict)
            if swim_pool == 'true': swim_pool = True
        except IndexError:
            swim_pool = False
        self.swimming_pool.append(swim_pool)

        try:
            state_of_the_bldg = jp.search('building.condition', self.temp_dict)
        except IndexError:
            state_of_the_bldg = None
        self.state_of_the_building.append(state_of_the_bldg)

       

    def create_csv(self) -> None: #Will save the csv on sys
        self.df = [self.locality, self.type_of_property,
                    self.subtype_of_property, self.price,
                    self.number_of_rooms, self.area_in_sq_meters,
                    self.fully_equipped_kitchen, self.terrace,
                    self.garden, self.swimming_pool,
                    self.state_of_the_building]

        self.my_df = pd.DataFrame(self.df)
        self.my_df = self.my_df.transpose()
        self.my_df.to_csv(r'./belgian_housing_data.csv',index=False,
                         header = ["locality","type_of_property",
                            "subtype_of_property","price","number_of_rooms",
                            "area_in_sq_meters","fully_equipped_kitchen",
                            "terrace","garden","swimming_pool",
                            "state_of_the_building"])
        print(self.my_df.shape)
        # with open("../export_dataframe.csv", "w", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(self.df)