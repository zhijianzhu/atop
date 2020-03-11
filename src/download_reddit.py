import praw
import pandas as pd
import datetime as dt

def get_date(created):
    return dt.datetime.strftime(dt.datetime.fromtimestamp(created),'%Y-%m-%d %H:%M:%S')


class reddit_downloader:
    def __init__(self,client_id='GPgr9rpYRfrtvg', \
                            client_secret='Me4UupPmmF5I_8UDwoFNFH3Hzrk', \
                            user_agent='redditdocdig', \
                            username='aavls', \
                            password='KillCoronaVirus'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password
    
    def get_posts(self):
        # client_id='GPgr9rpYRfrtvg', \
        #                     client_secret='Me4UupPmmF5I_8UDwoFNFH3Hzrk', \
        #                     user_agent='redditdocdig', \
        #                     username='aavls', \
        #                     password='KillCoronaVirus'
        reddit = praw.Reddit(client_id = self.client_id, 
                            client_secret = self.client_secret,  
                            user_agent = self.user_agent, 
                            username = self.username, 
                            password = self.password)

        subreddit = reddit.subreddit('Coronavirus')
        # top_subreddit = subreddit.top()
        top_subreddit = subreddit.top(limit=2000)

        topics_dict = { "title":[], 
                        "score":[], 
                        "id":[],
                        "url":[],
                        "comms_num": [],
                        "created": [],
                        "body":[],
                        "comments":[],
                        "is_original":[],
                        "score":[],
                        "upvote_ratio":[]}

        cnt = 0
        for submission in top_subreddit:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            # topics_dict["comments"].append([(c.author.name,c.body) for c in submission.comments if c is not None and isinstance(c, praw.models.reddit.comment.Comment) and c.author is not None])
            topics_dict["comments"].append([{'created':get_date(c.created), 'author':c.author.name,'body':c.body} for c in submission.comments if c is not None and isinstance(c, praw.models.reddit.comment.Comment) and c.author is not None])
            topics_dict["is_original"].append(submission.is_original_content)
            topics_dict['upvote_ratio'].append(submission.upvote_ratio)
            cnt+=1
            print('Downloaded %d posts'%cnt)

        print('Done all downloading, converting dict to dataframe')
        topics_data = pd.DataFrame(topics_dict)
        _timestamp = topics_data["created"].apply(get_date)
        topics_data = topics_data.assign(timestamp = _timestamp)

        print('Saving data as JSON')
        topics_data.to_json('../data/reddit_post.json')

if __name__ == "__main__":
    downloader = reddit_downloader()
    downloader.get_posts()

# for comment in reddit.subreddit('Coronavirus').stream.comments():
#     print('%s said: %s \n ***********\n'%(comment.author.name, comment.body))

# for submission in reddit.subreddit('all').stream.submissions():
#     print('%s said: %s \n ***********\n'%(submission.author, submission.selftext))

# stats=reddit.subreddit("Coronavirus").traffic()