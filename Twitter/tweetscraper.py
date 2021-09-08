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
        self.weekObtained = False
        self.lastUpdated = datetime.now()
    
    #Method to take all tweets from the usernames sent in the past two weeks
    def obtainWeekTweets(self):
        self.shouldUpdate()
        if not self.weekObtained:
            end_date = datetime.utcnow() - timedelta(days=7)
            tweet_dict = dict()
            for username in self.usernames:
                tweets = []
                for status in Cursor(api.user_timeline, id = username, include_rts = False, exclude_replies = True, tweet_mode = 'extended').items():
                    tweets.append([username, status.full_text, status.created_at])
                    if status.created_at < end_date:
                        break
                
                tweet_dict[username] = tweets
            
            # print(len(tweet_lst))
            # print(tweet_dict)
            self.weekTweets = tweet_dict
            self.weekObtained = True
            self.lastUpdated = datetime.now()
    
    def shouldUpdate(self):
        print(datetime.now() - self.lastUpdated)
        if datetime.now() - self.lastUpdated > timedelta(minutes=10): 
            self.weekObtained = False
            print("RERUNNING")


    #Returns all tweets that have mentioned the team name
    def findRelevantTeamTweets(self, Team):
        rel_tweets = dict()
        # for lst in self.weekTweets:
        #     for tweet in lst:
        #         if Team.lower() in tweet.lower():
        #             rel_tweets.append(tweet)
                
        # return rel_tweets
        for user in self.usernames:
            lst_of_tweets = []
            user_tweets = self.weekTweets[user]
            for lst in user_tweets:
                
                if Team.lower() in lst[1].lower():
                    # print(lst)
                    lst_of_tweets.append(lst)
            # print(lst_of_tweets)
            rel_tweets[user] = lst_of_tweets
        # print(rel_tweets)
        return rel_tweets

    #Returns all tweets that have mentioned the player name
    def findRelevantPlayerTweets(self, Player):
        rel_tweets = dict()
        for user in self.usernames:
            lst_of_tweets = []
            user_tweets = self.weekTweets[user]
            for lst in user_tweets:
                
                if Player.lower() in lst[1].lower():
                    #print(lst)
                    lst_of_tweets.append(lst)
            rel_tweets[user] = lst_of_tweets
        # print(lst_of_tweets)
        # print(rel_tweets)
        return rel_tweets
    
    def obtainTweetsAboutPlayer(self, Player):
        search_word = Player + " -filter:retweets" + " -filter:replies"
        today = date.today()
        week_ago = today - timedelta(days=7)
        # print(week_ago)
        tweets = Cursor(api.search, q=search_word, lang = "en", since = week_ago).items(10)

        tweet_lst = []
        for tweet in tweets:
            # print(tweet.user.screen_name)
            # print(tweet.text)
            # tweet_lst.append(f'@{tweet.user.screen_name}: {tweet.text}')
            tweet_lst.append([f'@{tweet.user.screen_name}', tweet.text, tweet.created_at])
            
            # print("-------------------------------------------------")

        # print(tweet_lst)
        return tweet_lst
#TESTER CODE
# ts = tweetscraper()
# ts.obtainWeekTweets()
# ts.findRelevantTeamTweets("Arsenal")
# ts.findRelevantPlayerTweets("Messi")
# ts.obtaintweets()
# ts.obtainWeekTweets()
# ts.findRelevantTeamTweets('Chelsea')
# ts.findRelevantPlayerTweets('Lionel Messi')