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
        self.obtainWeekTweets()
    
    def obtainWeekTweets(self):
        end_date = datetime.utcnow() - timedelta(days=7)
        # print(end_date)
        tweet_lst = []
        for username in self.usernames:
            tweets = []
            for status in Cursor(api.user_timeline, id = self.usernames[0], include_rts = False, exclude_replies = True, tweet_mode = 'extended').items():
                # print(type(status))
                # print(status.full_text)
                tweets.append('@' + username + ": " + status.full_text)

                if status.created_at < end_date:
                    break
            
            tweet_lst.append(tweets)
        
        # print(len(tweet_lst))
        self.weekTweets = tweet_lst
    
    def findRelevantTeamTweets(self, Team):
        rel_tweets = []
        for lst in self.weekTweets:
            for tweet in lst:
                if Team.lower() in tweet.lower():
                    rel_tweets.append(tweet)
                
        return rel_tweets
                    
        
    def findRelevantPlayerTweets(self, Player):
        rel_tweets = []
        for lst in self.weekTweets:
            for tweet in lst:
                if Player.lower() in tweet.lower():
                    rel_tweets.append(tweet)
        
        return rel_tweets

# ts = tweetscraper()
# ts.obtaintweets()
# ts.obtainWeekTweets()
# ts.findRelevantTeamTweets('Chelsea')
# ts.findRelevantPlayerTweets('Lionel Messi')