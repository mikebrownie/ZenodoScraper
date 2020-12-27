# Zenodo Scraper
Challenge for The Collaboratory

### How does it work?
- Uses the Open Archives Initiative Protocol for Metadata Harvesting ([OAI- PMH](http://www.openarchives.org/pmh/)). 
- Unlike the Zenogo's REST API, it uses sets to allow for selective harvesting.
	-  `openaire_data` is our set of interest, contains all datasets
	- No need for Tokens or dealing with Zenogo REST API
## Files Included:
 1) `main.py` - Implementation of scraper, run it to start scraping!

### Output files:
 2) `result.JSON` - Harvested data from every Dataset formatted as:
 ```
 {  
"zenodo_id": {  

"link": "Working link to record",  
"title": "Dataset title",  
"date": "YYYY-MM-DD formatted date",  
"authors": [  

{  

"name": "Author1 Name, if available.",  
"affiliation": "University of Author, if available. If not available do not include this key."  

},  
{  
"name": "Author2 Name"  
"affiliation": "University of Author2"  
}  
...  

],  
"zenodo_id": "Unique zenodo identifier. Same as key for this entry."  

},  
...  

}
```
- 

3) `log.txt` - A log of unique identifiers of all datasets read by program. Used mostly for debugging.

### Example output



### Future Ideas:
- Cache responses in a local directory to save time on subsequent runs.
- Try using REST API and ElasticSearch queries to allow a batch size of 10,000 dataSets. 
	- Most likely using a moving date window. 
	- Could speed up initial run time, considering 100x improvement in batch size.
- Explore multi-threaded solution with a requester and resolver thread-pool to speed up initial run.



> Written with [StackEdit](https://stackedit.io/).
