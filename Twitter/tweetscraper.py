import tweepy
from tweepy import Cursor
from dotenv import load_dotenv
import os
from datetime import datetime, date, time, timedelta

#Setup .env file
load_dotenv()

#environment variables to protect the keys
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

#Authenticate itself on twitter
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)
# count = 25

class tweetscraper:
    #Usernames of twitter accounts to take tweets from
    usernames = ['FabrizioRomano', 'David_Ornstein']
    def __init__(self):
        # self.count = count
        self.usernames = tweetscraper.usernames
        self.obtainWeekTweets()
    
    #Method to take all tweets from the usernames sent in the past two weeks
    def obtainWeekTweets(self):
        end_date = datetime.utcnow() - timedelta(days=7)
        tweet_lst = []
        for username in self.usernames:
            tweets = []
            for status in Cursor(api.user_timeline, id = self.usernames[0], include_rts = False, exclude_replies = True, tweet_mode = 'extended').items():
                tweets.append('@' + username + ": " + status.full_text)

                if status.created_at < end_date:
                    break
            
            tweet_lst.append(tweets)
        
        # print(len(tweet_lst))
        self.weekTweets = tweet_lst
    
    #Returns all tweets that have mentioned the team name
    def findRelevantTeamTweets(self, Team):
        rel_tweets = []
        for lst in self.weekTweets:
            for tweet in lst:
                if Team.lower() in tweet.lower():
                    rel_tweets.append(tweet)
                
        return rel_tweets
                    
    #Returns all tweets that have mentioned the player name
    def findRelevantPlayerTweets(self, Player):
        rel_tweets = []
        for lst in self.weekTweets:
            for tweet in lst:
                if Player.lower() in tweet.lower():
                    rel_tweets.append(tweet)
        
        return rel_tweets

#TESTER CODE
# ts = tweetscraper()
# ts.obtaintweets()
# ts.obtainWeekTweets()
# ts.findRelevantTeamTweets('Chelsea')
# ts.findRelevantPlayerTweets('Lionel Messi')