#!/usr/bin/env python
# encoding: utf-8
#Author - Prateek Mehta


import tweepy #https://github.com/tweepy/tweepy
import json


#!/usr/bin/env python
# encoding: utf-8

import tweepy
import json
import twitter_credentials

def get_all_tweets(event):
#Twitter API credentials
    auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweet

    #keep grabbing tweets until there are no tweets left to grab
    searched_tweets = []
    last_id = -1
    max_tweets = 10
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=event+ '-filter:retweets -filter:replies', count=count, max_id=str(last_id - 1),Since="2019-09-09",tweet_mode="extended",include_rts =False,exclude_replies=True,lang="en")
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            break
    print ("...{} tweets downloaded so far".format(len(searched_tweets)))
    tweets = [[tweet.full_text] for tweet in searched_tweets]
    print(tweets)
    #write tweet objects to JSON
    file = open('tweettext.json', 'w')
    print ("Writing tweet objects to JSON please wait...")
    json.dump(tweets,file)
    #close the file
    print ("Done")
    file.close()

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("celtics")
