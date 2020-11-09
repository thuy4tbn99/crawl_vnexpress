# crawl_vnexpress

# Overview
Use https://scrapy.org/ to crawl data from Vnexpress.net  
Folder vnexpress crawl with scrapy-splash  
Folder scrapy_vnexress use only scrapy  
# Scrapy_vnexpress
This project only focus on category 'thoi-su' (news category)  
Crawl ~ 10000 article with title, date, tags, content with vnexpress_spider.py  
It crawls comment in each article with comment_spider.py  
It crawls all comment from each user who vnexpress_spider got id  
# Setup for scrapy_vnexpress  
pip install scrapy 
