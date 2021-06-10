from crawler import crawler
from visualization import vis
from pathlib import Path
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

root_path = str(Path(__file__).parent.absolute())
#load df from pickle file.
PATH_TO_PICKLE  = root_path + '/data/articles.pkl'

def main():
    print("Start")
    
    
    #Update data
    crawler.crawl_data(root_path)


    df = pd.read_pickle(PATH_TO_PICKLE)
    df_task_two = pd.read_pickle(PATH_TO_PICKLE) 

    '''
       Task 2 
    '''
    df_task_two.set_index('date', inplace=True)
    df_task_two = pd.DataFrame({'Anzahl Artikel' : df_task_two.groupby(df_task_two.index.date).size() }) \
        .reset_index() \
        .rename(columns = {'index':'Datum'})
    print('\n \n Task 2 \n')
    print(df_task_two.to_string())
    df_task_two.to_csv(f'{root_path}/data/export/task_2.csv')
    
    # days passed since 2018-01-01
    d0 = date(2018, 1, 1)
    d1 = date.today()
    interval = d1 - d0
    numb_of_days = interval.days

    # the sum is the same as the numb of columns in the original df
    mean = df_task_two['Anzahl Artikel'].sum()/numb_of_days
    pd.Series(mean).to_string(f'{root_path}/data/export/task_3-mean.txt')
    print('mean: ' + str(mean))

    '''
        Task 4
    '''
    # The resulting object of '.value_counts()' is in descending order so that the first element is the most frequently-occurring element
    print('\n Task 4 \n Anzahl der Artikel über Justin Trudeu in der jeweiligen Section.')
    df_task4= pd.DataFrame(df['sectionName'].value_counts())
    print(df_task4)
    df_task4.to_json(f'{root_path}/data/export/task_4.json', indent=2)
    
    '''
       Task 5
    '''

    task_05(False)
    

    '''
       Task 8
    '''
    # collect evidence for detected events

    #Peak 06-2018
    df_2018_jun = df.set_index(df['date']).loc['2018-06-01':'2018-06-30'].reset_index(drop=True)

    #Peak 09/10-2019
    df_2019_sep_oct = df.set_index(df['date']).loc['2019-09-01':'2019-10-31'].reset_index(drop=True)

    #Intervall 01/03-2019
    df_2019_jan_march = df.set_index(df['date']).loc['2019-01-01':'2019-03-31'].reset_index(drop=True)

    #Intervall 03-2029 to 04-2021
    df_2020_march_jun = df.set_index(df['date']).loc['2020-03-01':'2021-04-30'].reset_index(drop=True)

    
    #exports
    df_2018_jun[['headline', 'trailText']].to_json(root_path + '/data/evidence/2018_june.json', orient='records', indent=2)
    df_2019_sep_oct[['headline', 'trailText']].to_json(root_path + '/data/evidence/2019_sep-oct.json', orient='records', indent=2)
    df_2019_jan_march[['headline', 'trailText']].to_json(root_path + '/data/evidence/2019_jan-march.json', orient='records', indent=2)
    df_2020_march_jun[['headline', 'trailText']].to_json(root_path + '/data/evidence/2020-jan_to_2021-april.json', orient='records', indent=2)

def task_05(update_date=True):
    '''
       Task 5
    '''
    if update_date:
        #Update data
        crawler.crawl_data(root_path)


    #readFile
    df = pd.read_pickle(PATH_TO_PICKLE) 
    
    df.set_index('date', inplace=True)
    df = pd.DataFrame({'Anzahl Artikel' : df.groupby(df.index.date).size() }) \
        .reset_index() \
        .rename(columns = {'index':'Datum'})

    df['Datum'] = pd.to_datetime(df['Datum'], format='%Y-%m-%d')
    df = df.groupby(pd.Grouper(key='Datum',freq='M')).sum() \
        .reset_index() \
        .rename(columns = {'index':'Datum'})
    
    month_series =pd.Series(pd.date_range(start="2018-01-01", end=date.today() + relativedelta(months=1), freq="M")) # every month from 2018-01 until he current month.

    
    df_to_vis= pd.concat([month_series, df], join='outer', axis=1 ) # add missing dates (month in which no articles were released), columnwise.
    del df_to_vis['Datum'] # rm old Datum column
    df_to_vis.rename(columns={0: 'Datum'}, inplace=True) 
    df_to_vis.fillna(.0, inplace=True) #NaN -> 0.0

    df_to_vis['Datum'] = df_to_vis['Datum'].dt.to_period('M') #aggregate information for vis
    
    # handle x axis content.
    df_to_vis['Datum'] = df_to_vis['Datum'].map(lambda x: x if str(x).split('-')[1] == '01' else str(x).split('-')[1]) 

    vis.bar_chart(df_to_vis, root_path)

if __name__ == "__main__":
    main()
