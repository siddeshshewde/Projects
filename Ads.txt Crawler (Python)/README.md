<h1 align="center">Ads.txt Crawler (Python)</h1>
 
## Introduction
A Simple crawler for ads.txt files given a list of URLs or domains and save them to csv as well as sqlite db.

- Crawling of Ads.txt URL using requests module (in Python).
- Storing parsed lines in a csv.
- Storing parsed lines in sql db (sqlite3).
- Required error handling and also storing error logs (sqlite3).

## Installation
The project depends on the below programs and packages:
- Python 3 or higher (Works on python 2 as well with minor syntax changes)
- Python HTTP requests library
```
>>> pip install requests
```
- Python tld module
```
>>> pip install tld
```
- SQLite3 or directly import the db file here: https://sqliteonline.com/

## Running
The application was tested with python 3.7.4, so make sure you are using the right version. Program should run on python 2.x as well with minor modifications in syntax.
```
>>> python adstxt_crawler_using_list.py
```
If the domain list is huge (1000+ domains) then use:
```
>>> python adstxt_crawler_using_set.py
```
The output is stored in a csv (Crawled Domains.csv) or database (ads_txt.ads_txt).

You can examine the DB records created as follows:
```
select * from ads_txt.ads_txt
```
You can clear the DB records as follows:
```
delete from ads_txt.adstxt;
```

## Target File, Database and Table Details
Database    : ads_txt (.db) | variable=connection

Target File : Crawled Domains (.csv) | variable=target_file

Table Name  : ads_txt | variable=create_stmt

Domain List : Domain List (.csv) | variable=csv_domain_list


## Warnings
- If the output file is not deleted before running another crawler, the file will be replaced.
- This is an example prototype crawler and would be suitable only for a very modest production usage. It doesn't contain a lot of niceties of a production crawler, such as parallel HTTP download and parsing of the data files, stateful recovery of target servers being down, usage of a real production DB server etc.

## Contributers
Initial Author is Siddesh Shewde.
