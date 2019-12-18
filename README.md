

# Overview

This is written in Python. There is still a lot of work to do, so feel free to help out with development. It takes around 1 hour to fetch all inventory , multithreading can improve the performance

COUPLE OF VAUES ARE HARDCODE WHICH ARE NOTHING JUST CLASS NAME OF HTML TAGS, IT WILL CHANGE WHENEVER THEY DO THE NEXT DEPLOYMENT, SO WE HAVE TO CHANGE ACCORDINGLY


###

How to run?

Project os developed in python 3.x


1) Install python 3.x and compatible scrapy

https://scrapy.org/download/ 

2) Go to main folder of project

3) Run 

scrapy crawl quotes

or 

scrapy crawl quotes -a url='https://sg.abc.com/'

or if you want to run in background

scrapy crawl quotes -a url='https://sg.sbc.com' > 404.txt &


output file will be there in main folder with time stamp.

####

STATS

We get various error during processing, these are details 


 'downloader/request_count': 25765,

 'downloader/request_method_count/GET': 25765,

 'downloader/response_bytes': 2694189714,

 'downloader/response_count': 25761,

 'downloader/response_status_count/200': 25432,

 'downloader/response_status_count/404': 73,

 'downloader/response_status_count/500': 30,

 'downloader/response_status_count/502': 3,

 'downloader/response_status_count/503': 14,

 'downloader/response_status_count/504': 209,



Important Note 

There are 25K inventory in car category and we are making request from same IP, they may disable in future.

 
 
******************************************* END   ***************************************

