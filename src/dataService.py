import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
from re import findall
import requests 
import plotly.express as px


class dataServiceCSSE:

    def __init__(self):
        
        self.today = date.today()  # check wether date changed 
        self.categories = ['Confirmed','Deaths','Recovered']
        self.region_of_interest = ['US', 'Germany', 'Italy', 'United Kingdom'
                          , 'Canada', 'Iran','Spain'
                          ,'China'
                          ,'Japan'
                          ,'Singapore'
                          ,'Australia'
                          ]
        self.init_datasSet()

    def regions (self ):
        return self.region_of_interest

    def init_datasSet(self):
        # Fetch data 
        self.dataSet = {}
        for category in self.categories:
            self.dataSet[category] = pd.read_csv( \
                                        self.dataSource(category),
                                        error_bad_lines=False) 

        self.all_date_range = self.init_date_range(self.dataSet[category])


    def dataSource(self,category:int) -> str:
        '''
        Return the URL for the given category, which is one of the following:
        Confirmed, Deaths, Recovered
        
        Return None if the given parameter is none of the above three.

        '''
        base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"



        dataSources = {'Confirmed':'time_series_19-covid-Confirmed.csv',
                       'Deaths':'time_series_19-covid-Deaths.csv',
                       'Recovered':'time_series_19-covid-Recovered.csv'}
        
        fn = dataSources.get(category)
        
        return base_url+fn if fn else fn 


    def init_date_range(self,df):
        # if ALL_DATES already populated, use it directdly in the same day 

        # otherwiese populate it 
        date_list = df.columns.to_list()

        return date_list[4:]


    def date_range(self, date_window_option = 'ALL'):
        # ALL, MONS, MON, WEEKS, WEEK
        # format- m/d/yy

        if date_window_option == 'ALL':
            return self.all_date_range

        dtDelta = { 'MONS':60, 'MON':30, 'WEEKS':14, 'WEEK':7}

        ret = []
        for d in range( dtDelta[date_window_option], 0, -1):
            dt = self.today - timedelta(days=d)
            ret.append( '{}/{}/{}'.format(dt.month, dt.day, dt.year % 100))

        return ret

    def refresh_data(self, date_window_option, region_of_interest):
        # refresh data as per :category, date list and region of interest 

        date_list = self.date_range( date_window_option)
        ret = []
        for category in ['Confirmed','Deaths','Recovered']:
            ret.append( self.refresh_catetgory(category, 
                date_list,
                region_of_interest
                ))

        return ret[0], ret[1], ret[2],' {} ~ {}'.format(date_list[0], date_list[-1])


    def refresh_catetgory( self, category, date_list, region_of_interest):
        
        df = self.dataSet[category]
        
        ret = []
        for region in region_of_interest:
            #print("region is ", region)
            df_1 = df[df['Country/Region'] == region]
            df_1 = df_1.fillna(0)

            counts = list(np.sum(np.array(df_1[date_list]), axis=0))
            counts = [int(x) for x in counts]
            ret.append({'x': date_list, 'y': counts, 'mode': 'lines+markers', 'name': region})

        return ret 





class dataServiceCSBS:

    def __init__(self):
        
        self.today = date.today()  # check wether date changed 
        self.categories = ['Confirmed','Deaths']
        self.all_date_range=[]
        self.df_columns=['County_Name','State_Name',
                         'Confirmed','New',
                         'Death','Fatality_Rate',
                         'Latitude','Longitude',
                         'Last_Update']
        self.init_datasSet()


    def regions (self ):
        return self.region_of_interest

    def init_regions(self, Confirmed):
        # 
        s = Confirmed[['State_Name','2020-03-24']].groupby(['State_Name'])\
              .sum().sort_values('2020-03-24', ascending=False)
        self.region_of_interest = s.index.tolist() # [0:17]


    def init_datasSet(self):

        git_master_url = "https://github.com/tomquisel/covid19-data/tree/master/"

        csv_base_url = 'https://raw.githubusercontent.com/tomquisel/covid19-data/master/' 

        csvs = findall('data/csv/2020-0[0-9-]{4}.csv',
                          requests.get( git_master_url+'data/csv/').text )


        self.all_date_range = []
        Confirmed = pd.read_csv(csv_base_url+csvs[0], error_bad_lines=False)

        #Confirmed.set_index(['County_Name','State_Name'], inplace=True)

        Death = Confirmed.copy() 

        for csv in csvs:

            fn = csv_base_url + csv 
            data = pd.read_csv(fn, error_bad_lines=False)
            date = csv[9:-4] # # 2020-mm-dd  

            print(Confirmed.columns)
            c = data[['County_Name','State_Name','Confirmed']]
            c.columns = [ 'County_Name','State_Name',date]

            Confirmed = pd.merge( Confirmed, c,
                                        how='left',
                                        on=['County_Name','State_Name'])

            d = data[['County_Name','State_Name','Death']]
            d.columns = c.columns 
            Death = pd.merge( Death,d, how='left',
                                        on=['County_Name','State_Name'])

            self.all_date_range.append(date) 

        self.dataSet = {}
        self.dataSet[self.categories[0]] = Confirmed
        self.dataSet[self.categories[1]] = Death

        self.latest_date = self.all_date_range[-1]

        self.init_regions(Confirmed)


    def date_range(self, date_window_option = 'ALL'):
        # ALL, MONS, MON, WEEKS, WEEK
        # format- m/d/yy

        if date_window_option == 'ALL':
            return self.all_date_range

        dtDelta = { 'MONS':60, 'MON':30, 'WEEKS':14, 'WEEK':7}

        ret = []
        for d in range( dtDelta[date_window_option], 0, -1):
            dt = self.today - timedelta(days=d)
            ymd = '{}-{:02}-{:02}'.format(dt.year, dt.month, dt.day, dt.year)
            if ymd in self.all_date_range:
                ret.append(ymd)

        return ret

    def refresh_catetgory(self, category:str, date_window_option, region_of_interest):
        # refresh data as per :category, date list and region of interest 
        df = self.dataSet[category]

        self.date_list = self.date_range( date_window_option)

        ret = []
        for region in region_of_interest:
            #print("region is ", region)
            df_1 = df[df['State_Name'] == region]
            df_1 = df_1.fillna(0)

            counts = list(np.sum(np.array(df_1[self.date_list]), axis=0))
            counts = [int(x) for x in counts]
            ret.append({'x': self.date_list, 'y': counts, 
                'mode': 'lines+markers', 'name': region})

        return ret 

    def date_range_str(self, date_window_option='ALL'):

        self.date_list = self.date_range( date_window_option)

        return '{}~{}'.format(self.date_list[0],self.date_list[-1]) 


    def geo_layout(self , title, projection='natural earth' ): #Confirmed Total
        layout = dict(title='CoronaVirus {} as of {}'.format(title, str(date.today())),
            height=700,
            colorbar=True,
            geo=dict(
                # scope='usa',
                projection=projection,  # dict( type='albers usa' ),
                showland=True,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
            )
        return layout 



    def geo_data(self, category):
        
        df = self.dataSet[category].fillna(0)
        df.drop(columns = ['County_Name','Confirmed', 'New', 'Death',
                   'Fatality_Rate', 'Last_Update', ], inplace=True)

        total = df.groupby('State_Name').sum()
        avg = df.groupby('State_Name').mean()

        total.reset_index(level=0, inplace=True)

        total['text'] = total.apply( lambda x: '{}\n{}'.format(x['State_Name'], x[self.latest_date]),axis=1)

        data = [dict(
            type='scattergeo',
            # locationmode =  #'USA-states',
                locations="iso_alpha",
                lon=avg['Longitude'],
                lat=avg['Latitude'],
                text=total['text'],
                mode='markers',
                marker=dict(
                    size=8,
                    opacity=0.8,
                    reversescale=True,
                    autocolorscale=False,
                    symbol='circle',
                    line=dict(
                        width=1,
                        color='rgba(102, 102, 102)'
                    ),
                    # colorscale = scl,
                    color_continuous_scale=px.colors.diverging.BrBG,
                    color_continuous_midpoint=avg[self.latest_date],
                    cmin=0,
                    color=total[self.latest_date],
                    cmax=total[self.latest_date].max(),
                    colorbar=dict(
                        title=' {} Total'.format(category) 
                    )
                ))]

        return data 
 
#ds = dataServiceCSSE()

ds = dataServiceCSBS()
