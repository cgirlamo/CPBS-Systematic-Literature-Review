# CPBS-Systematic-Literature-Review
## file structure  
|--.boolean - this is the python environment  
|-- Scopus/ - csv outputs with article info for Scopus  
|-- Boolean_keywords.xlsx - excel sheet with original keywords, and initial boolean search strings   
|-- export_scopus.ipynb - jupyter notebook to export scopus results from SQL DB to csv files  
|-- IEEE.py - python script to scrape IEEE API - not functional  
|-- make_keywords.ipynb - jupyter notebook to make boolean search strings from keywords  
|-- results.xlsx - boolean search strings, updates when make_keywods.ipynb is run  
|-- Scopus_getauthor.py - python script to get all authors, not just the first one  
|-- Scopus_results.csv - csv with the number of papers each boolean search string returned  
|-- Scopus.py - script to scrape Scopus API  
|-- test_json.ipynb - jupyter notebook to fool about with .json outputs  
|-- test.json - example of Scopus JSON returned  
|-- testing.md - test workspace for boolean search strings  
|-- WoS_results.csv - home for WoS counts of articles boolean searches returned  
|-- Script to scrape WoS API - currently empty  