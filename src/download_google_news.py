import newsapi
import datetime as dt
import json
import os

class google_news_downloaded:
    def __init__(self, api_key='33e5769ae6964b55bcd6b987adc73c86', \
                 path='../data/google_news/', \
                 hours_gap=1, \
                 minutes_gap=0, \
                 daily_limit=250):
        self.api_key = api_key
        self.path = path
        self.hours_gap = hours_gap
        self.minutes_gap = minutes_gap
        self.daily_limit = daily_limit

    def get_news(self):
        news = newsapi.NewsApiClient(self.api_key)
        current_time = dt.datetime.utcnow()
        start_time = dt.datetime.strptime(max(os.listdir(self.path)).split('.')[0],'%Y-%m-%dT%H%M%S')
        i = 0
        while (i < self.daily_limit and start_time + dt.timedelta(hours = self.hours_gap, minutes = self.minutes_gap) <= current_time): 
            i += 1
            start_time += dt.timedelta(hours = self.hours_gap, minutes = self.minutes_gap)
            all_articles = news.get_everything(q = 'coronavirus',
                                                  from_param = start_time.isoformat(timespec = 'seconds'),
                                                  to = (start_time + dt.timedelta(hours = self.hours_gap, minutes = self.minutes_gap)).isoformat(timespec = 'seconds'),
                                                  language = 'en',
                                                  page_size = 100,
                                                  page = 1)
            f = open(self.path + start_time.isoformat(timespec = 'seconds').replace(':','') + '.json', 'w')
            f.write(json.dumps(all_articles['articles']))
            f.close()
            
    def get_old_news(self):
        news = newsapi.NewsApiClient(self.api_key)
        end_time = dt.datetime.strptime(min(os.listdir(self.path)).split('.')[0],'%Y-%m-%dT%H%M%S')
        i = 0
        while (i < self.daily_limit): 
            i += 1
            start_time = end_time - dt.timedelta(hours = self.hours_gap, minutes = self.minutes_gap)
            try:
                all_articles = news.get_everything(q = 'coronavirus',
                                                          from_param = start_time.isoformat(timespec = 'seconds'),
                                                          to = end_time.isoformat(timespec = 'seconds'),
                                                          language = 'en',
                                                          page_size = 100,
                                                          page = 1)
                end_time -= dt.timedelta(hours = self.hours_gap, minutes = self.minutes_gap)
                f = open(self.path + start_time.isoformat(timespec = 'seconds').replace(':','') + '.json', 'w')
                f.write(json.dumps(all_articles['articles']))
                f.close()
            except newsapi.newsapi_exception.NewsAPIException:
                print('daily limit reached')
                break
                
if __name__ == "__main__":
    downloader = google_news_downloaded()
    downloader.get_news()
    #downloader.get_old_news()
