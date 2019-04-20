#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:38:01 2019

@author: anurags
"""

import scrapy
from .car import Car;
import json;
from datetime import datetime


class QuotesSpider(scrapy.Spider):
    name = "quotes";
    #base_url = "https://sg.carousell.com/";
    datafile = None;
    
    FIRST_PAGE_PRODUCT_CLASS_NAME = 'bM-U';
    TITLE_CLASS_NAME = 'bM-m';
    PRICE_CLASS_NAME = 'bM-k';
    
    PRODUCT_DETAIL_CLASS_NAME = 'ay-c ay-b';
    LIST_CLASS_NAME = 'bB-l';


    start_urls = [
        'https://sg.carousell.com/categories/cars-32/',
    ]

   
    def __init__(self):
        today = datetime.now();
        self.datafile = open(today.strftime("%Y_%m_%d_%H_%M_%S"), 'w');
    
    def __del__(self): 
        self.datafile.close();
        
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        
        for quote in response.xpath("//div[@class='{}']".format(self.FIRST_PAGE_PRODUCT_CLASS_NAME)):
            car = Car();
            
            car.title = quote.xpath(".//div[@class='{}']/text()".format(self.TITLE_CLASS_NAME)).extract_first();
            #print(car.title)
            
            #car.posted_on = quote.xpath(".//time[contains(@class,'{}')]/span/text()".format(self.POSTED_CLASS_NAME)).extract_first();
            car.posted_on = quote.xpath(".//a/div/time/span/text()").extract_first();
            #print(car.posted_on);
            
            car.seller = quote.xpath(".//a/div/div/text()").extract_first();
            #print(car.seller);
            
            car.price =  quote.xpath(".//div[@class='{}']/div/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            #print(car.price)
            
            reg_year = quote.xpath(".//div[@class='{}']/div[2]/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            
            try:
                if reg_year.index("Reg: ") == 0:
                    car.reg_year = reg_year[5:len(reg_year)];
                    #print(car.reg_year);
            except:
                pass;
                
                
            
            depre = quote.xpath(".//div[@class='{}']/div[3]/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            
            try:
                if depre.index("Depre: ") == 0:
                    car.depre = depre[7:len(depre)];
                    #print(car.depre);
            except:
                pass;
            
            #svg = quote.xpath("boolean(.//svg[contains(@class, '{}')])".format(self.BOOSTED_CLASS_NAME)).extract_first();
            car.boosted = quote.xpath("boolean(.//a/div/time/svg)").extract_first();
            #print(car.boosted);
            
            link = quote.xpath(".//figcaption/a/@href").extract_first();
            #print(link);
            car.listingId  = link.split("/")[2].split('-')[-1];
            
            product_url = response.urljoin(link);
            yield scrapy.Request(product_url, callback=self.parseProduct, meta={'item': car});
            
        
        # handle next page
        next_page = response.xpath("//ul[@class='pager']/li[contains(@class, 'pagination-next')]/a/@href").extract_first();
        next_page_url = response.urljoin(next_page);
        #print(next_page_url)
        #yield scrapy.Request(next_page_url, callback=self.parse);
        
        
    
    def parseProduct(self, response):
        #print(response.url);
        car = response.meta['item'];
         
        for product in response.xpath("//div[@class='{}']/section".format(self.PRODUCT_DETAIL_CLASS_NAME)):
            header_name = product.xpath(".//h2/text()").extract_first();
            #print("Header name: " + str(header_name));
            
            
            if header_name == "Car Details":
                for detail in product.xpath(".//div[@class='{}']".format(self.LIST_CLASS_NAME)):
                #for detail in product.xpath(".//div[contains(@class, '-')]/div"):
                    label = detail.xpath(".//label/text()").extract_first();
                    #print("Label: " + str(label))
                    
                    if label == "Mileage":
                        car.mileage = detail.xpath(".//p/text()").extract_first();
                        #print(car.mileage)
                        
                    if label == "COE Expiry":
                        car.coe_expiry = detail.xpath(".//p/text()").extract_first();
                        #print(car.coe_expiry);
                        
                    if label == "Engine Capacity (cc)":
                        car.engine_capicity = detail.xpath(".//p/text()").extract_first();
                        #print(car.engine_capicity)
        
            
        #print(car);
        
        # write car object in file
        self.datafile.write(str(car));
        self.datafile.write(' ')
        return;

    
   
        
        
        



