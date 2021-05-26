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

class websc:
    
    #defining the attributes of each property
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
    df = pd.DataFrame()

    def change_my_page(self, nbr):
        self.page_number = nbr
        self.search_url = (f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&propertySubtypes=BUNGALOW,CHALET,FARMHOUSE,CASTLE,COUNTRY_COTTAGE,EXCEPTIONAL_PROPERTY,APARTMENT_BLOCK,MIXED_USE_BUILDING,TOWN_HOUSE,MANSION,VILLA,OTHER_PROPERTY,MANOR_HOUSE,PAVILION,GROUND_FLOOR,DUPLEX,TRIPLEX,FLAT_STUDIO,PENTHOUSE,LOFT,SERVICE_FLAT,KOT&page={nbr}&orderBy=relevance")

    def crawl(self):
        for i in self.data:
            for k,v  in enumerate(i):
                if v == 'classified':
                    self.temp_dict = list(i.items())[k][1]
                    self.parse_data(self.temp_dict)

                    
    def parse_data(self, new_dict):
    #parsing json for reqd info

        try:
            rooms = jp.search('bedroom.count', new_dict)          
        except IndexError:
            rooms = None
        self.number_of_rooms.append(rooms)

        try:
            state_of_the_bldg = jp.search('building.condition', new_dict)
            #print('state = ',state_of_the_bldg)
        except IndexError:
            state_of_the_bldg = None
        self.state_of_the_building.append(state_of_the_bldg)

        try:
            kitchen= jp.search('classified.kitchen.type', new_dict)
            #print('kitchen = ',kitchen)
        except IndexError:
            kitchen = None
        self.fully_equipped_kitchen.append(kitchen)

        #making a list of lists    
        self.df_list.append(pd.DataFrame({'Rooms': self.number_of_rooms,
                            'State of building': self.state_of_the_building,
                            'Fully equipped kitchen': self.fully_equipped_kitchen},
                             index = [[0]]))

        self.create_data_frame()
        

    def create_data_frame(self):
        
        #adding to data frame
        self.df = pd.concat(self.df_list, ignore_index=True, sort=False)
        print(self.df)

    
