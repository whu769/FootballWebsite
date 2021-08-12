import tweepy
from tweepy import Cursor
from dotenv import load_dotenv
import os
from datetime import datetime, date, time, timedelta

load_dotenv()
#environment variables

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)
# count = 25

class tweetscraper:
    usernames = ['FabrizioRomano', 'David_Ornstein']
    def __init__(self):
        # self.count = count
        self.usernames = tweetscraper.usernames

    def obtaintweets(self):
        lst_of_tweets = []
        for username in self.usernames:
            try:
                tweets = api.user_timeline(screen_name = username, count = self.count, exclude_replies = False, include_rts = False,
                                            tweet_mode = 'extended')
            except Exception as e:
                print(f'Something Failed: {str(e)}')

            for tweet in tweets:
                if(tweet.full_text[0] == '@'):
                    continue
                else:
                    print(tweet.full_text)
                    print(tweet.id)
                    print("-------------------------------------------------------------------")
    
    def obtainWeekTweets(self):
        end_date = datetime.utcnow() - timedelta(days=7)
        print(end_date)
        tweet_lst = []
        for username in self.usernames:
            tweets = []
            for status in Cursor(api.user_timeline, id = self.usernames[0], include_rts = False, exclude_replies = True, tweet_mode = 'extended').items():
                # print(type(status))
                # print(status.full_text)
                tweets.append(status.full_text)

                if status.created_at < end_date:
                    break
            
            tweet_lst.append(tweets)
        
        # print(len(tweet_lst))
        self.weekTweets = tweet_lst

ts = tweetscraper()
# ts.obtaintweets()
ts.obtainWeekTweets()