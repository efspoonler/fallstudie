from pathlib import Path
from datetime import date
import requests
import time
import pandas as pd

API_ENDPOINT = 'http://content.guardianapis.com/search'

'''
https://content.guardianapis.com/search?
tag=world%2Fjustin-trudeau&
from-date=2018-01-01&
order-by=oldest&
show-fields=headline%2CtrailText%2Cwordcount&
api-key=KEY
'''



def crawl_data(root_path):
    '''
       create a new dataset
    '''
    #path_json = root_path + '/data/articles.json'
    path_pickle = root_path + '/data/articles.pkl'

    # get the key
    KEY = open(root_path + '/crawler/key.txt').read() #str
    
    #init GET params
    params = {
    'tag': 'world/justin-trudeau', # The latest news and comment on Justin Trudeau
    'from-date': "2018-01-01",
    #'to-date': date.today(),
    'order-by': "oldest", # by default -> use-date:published (The date the content has been last published)
    'show-fields': 'headline,trailText,wordcount',
    'page-size': 200, # 200 is the max value
    'api-key': KEY 
    }
    


    all_data_concat = []
    currentPage = 1
    pages = 1
    while currentPage <= pages:
            '''
                ATM one request is enough.
            '''
            response = requests.get(API_ENDPOINT, params)

            if response.status_code == 200:
                data = response.json()
                all_data_concat.extend(data['response']['results'])
                currentPage += 1 # point to the next page
                params['page'] = currentPage # retriev the next page by the following request
                pages = data['response']['pages'] # stays the same
            
                time.sleep(1)
            else:
                time.sleep(2)
                print('request will be executed again. status code: ' + str(response.status_code))

    df_preprocessed = _preprocessor(all_data_concat) # returns a DataFrame

    # save df to disk
    df_preprocessed.to_pickle(path_pickle) # pickle files retain the original state of the dataframe
    #df_preprocessed.to_json(path_json.head(), orient='records', indent=2) # for taking a look at the data

    print('The data is fully crawled and saved to a pickle file.')

def _preprocessor(data):
    '''
       - Select features for the task
       - create a dataframe
       - adapt dtypes
    '''
    
    # feature selection
    data_preprocessed = []
    for indx, article in enumerate(data):
        data_preprocessed.append({
            'id': article['id'],
            'type': article['type'],
            'sectionId': article['sectionId'],
            'sectionName': article['sectionName'],
            'date':article['webPublicationDate'], 
            'headline': article['fields']['headline'],
            'trailText': article['fields']['trailText'],
            'wordcount': int(article['fields']['wordcount'])
        })
    # list to DataFrame
    df = pd.DataFrame(data_preprocessed)

    # convert dtype of 'date' column
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
    return df    
