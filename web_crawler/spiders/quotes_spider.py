#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:38:01 2019

@author: anurags
"""

import scrapy
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
   
    def __init__(self, url='https://sg.carousell.com/categories/cars-32/', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url];
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
            item = {};
            
            item['title'] = quote.xpath(".//div[@class='{}']/text()".format(self.TITLE_CLASS_NAME)).extract_first();
            #print(item['title'])
            
            #car.posted_on = quote.xpath(".//time[contains(@class,'{}')]/span/text()".format(self.POSTED_CLASS_NAME)).extract_first();
            item['posted_on'] = quote.xpath(".//a/div/time/span/text()").extract_first();
            #print(item['posted_on']);
            
            item['seller'] = quote.xpath(".//a/div/div/text()").extract_first();
            #print(item['seller']);
            
            item['price'] =  quote.xpath(".//div[@class='{}']/div/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            #print(item['price'])
            
            reg_year = quote.xpath(".//div[@class='{}']/div[2]/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            
            try:
                if reg_year.index("Reg: ") == 0:
                    item['reg_year'] = reg_year[5:len(reg_year)];
                    #print(item.reg_year);
            except:
                pass;
                
                
            
            depre = quote.xpath(".//div[@class='{}']/div[3]/text()".format(self.PRICE_CLASS_NAME)).extract_first();
            
            try:
                if depre.index("Depre: ") == 0:
                    item['depre'] = depre[7:len(depre)];
                    #print(item.depre);
            except:
                pass;
            
            #svg = quote.xpath("boolean(.//svg[contains(@class, '{}')])".format(self.BOOSTED_CLASS_NAME)).extract_first();
            item['boosted'] = quote.xpath("boolean(.//a/div/time/svg)").extract_first();
            #print(item['boosted']);
            
            link = quote.xpath(".//figcaption/a/@href").extract_first();
            #print(link);
            item['listingId']  = link.split("/")[2].split('-')[-1];
            
            product_url = response.urljoin(link);
            yield scrapy.Request(product_url, callback=self.parseProduct, meta={'inventory': item});
            
        
        # handle next page
        next_page = response.xpath("//ul[@class='pager']/li[contains(@class, 'pagination-next')]/a/@href").extract_first();
        next_page_url = response.urljoin(next_page);
        #print(next_page_url)
        yield scrapy.Request(next_page_url, callback=self.parse);
        
        
    
    def parseProduct(self, response):
        #print(response.url);
        item = response.meta['inventory'];
         
        for product in response.xpath("//div[@class='{}']/section".format(self.PRODUCT_DETAIL_CLASS_NAME)):
            header_name = product.xpath(".//h2/text()").extract_first();
            #print("Header name: " + str(header_name));
            
            
            if header_name == "Car Details":
                for detail in product.xpath(".//div[@class='{}']".format(self.LIST_CLASS_NAME)):
                #for detail in product.xpath(".//div[contains(@class, '-')]/div"):
                    label = detail.xpath(".//label/text()").extract_first();
                    #print("Label: " + str(label))
                    
                    if label == "Mileage":
                        item['mileage'] = detail.xpath(".//p/text()").extract_first();
                        #print(item['mileage'])
                        
                    if label == "COE Expiry":
                        item['coe_expiry'] = detail.xpath(".//p/text()").extract_first();
                        #print(item['coe_expiry']);
                        
                    if label == "Engine Capacity (cc)":
                        item['engine_capicity'] = detail.xpath(".//p/text()").extract_first();
                        #print(item['engine_capicity'])
        
            
        #print(item);
        
        # write car object in file
        self.datafile.write(str(item));
        self.datafile.write(' ')
        return;

    
   
        
        
        



