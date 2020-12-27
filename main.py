# Author: Michael Brown
# Created for the Collaboratory Challenge, Web scraper for  Zenodo.org. no REST API.

import requests
import json
from bs4 import BeautifulSoup # makes parsing through markup languages easier
import time
import copy

# This solution uses Zenodos Open Archives Initiative Protocol (https://developers.zenodo.org/#oai-pmh) for Metadata Harvesting
# Source: http://www.openarchives.org/OAI/openarchivesprotocol.html

if __name__ == '__main__':
    base_url = 'https://zenodo.org/oai2d'
    params = {
        'verb': 'ListRecords',
        'metadataPrefix': 'oai_datacite',
        'set': 'openaire_data'  # this set contains all the datasets on Zenoga
    }
    response = requests.get(base_url, params=params)
    del params['set']  # ONLY specify set for initial request

    log = open("log.txt", 'w')
    totalReadCount = 0 #  how many records were read
    dataReadCount = 0 #  how many dataSets were read
    page = 0
    all_info = {}
    while(response.status_code == 200):
        page+=1
        print("page: {}".format(page))
        soup = BeautifulSoup(response.text, 'html.parser')  # file is XML but html parser works fin for our purposes
        records = soup.select('ListRecords record')
        # parse through each record
        for record in records:
            payload = record.select_one('metadata oai_datacite payload')
            # only want datasets
            if (payload.select_one('resourcetype[resourcetypegeneral="Dataset"]')):
                info = {}
                dataReadCount += 1
                #grabbing relevant data, storing in info dictionairy
                id = record.select_one('header identifier').text[15:]  # only want record id, dropping oai:zenodo.org: (15chars)
                date = payload.select_one('dates date').text
                title = payload.select_one('titles title').text
                info = {'zenodo_id': id,
                        'link': 'https://zenodo.org/record/'+id,  #https link?
                        'title': title,
                        'date': date,
                        }
                # Creating a list of Dictionaries of authors+affiliation if applicable
                author_dict = {}
                authors = []
                for creator in payload.select('creators creator'):
                    author_dict["name"] = creator.select_one('creatorName').text
                    if creator.select_one('affiliation'):
                        # print(creator.select_one('affiliation'))
                        author_dict['affiliation'] = creator.select_one('affiliation').text
                    authors.append(copy.deepcopy(author_dict))
                    author_dict.clear()
                info["authors"] = authors
                all_info[info['zenodo_id']] = copy.deepcopy(info)
                log.write("SAVING RECORD  id: {}, page: {}\n".format(id, page))
            totalReadCount+=1
        # No records left,
        if soup.select_one('resumptionToken') == None:
            print("All records searched")
            break
        params['resumptionToken'] = soup.select_one('resumptionToken').text # get token for next page
        print('next token: {}'.format(params['resumptionToken']))
        print('dataset reads: {}'.format(dataReadCount))
        print('total reads: {}\n'.format(totalReadCount))
        # time.sleep(10) # Zenodo.org/Robots.txt rules: 10 seconds between requests
        response = requests.get(base_url, params=params)

    print("response status: {}".format(response.status_code)) # print http error
    with open('result.json', 'w') as of:
        json.dump(all_info, of)
    print("JSON file created")

    of.close()
    log.close()


