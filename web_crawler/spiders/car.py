#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:30:06 2019

@author: anurags
"""

class Car:
    
    title = '';
    price = '';
    posted_on = '',
    boosted = '';
    reg_year = '';
    depre = '';
    seller = '';
    mileage = '',
    coe_expiry = '';
    engine_capicity = '';
    listingId = '';
    
    def __str__(self):
        return str(self.__dict__)
    
    def to_json(self):
        return {'title': self.title}
    
    
    
    
    