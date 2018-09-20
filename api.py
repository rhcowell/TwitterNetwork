import tweepy
import json
import time
import logging

with open('api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)


def limit_handled(cursor):
    """
    handles the rate limit of Twitter API
    waits until rate limit time expires (15 min)
    :param cursor: Cursor object from Tweepy (includes API method and its params)
    :return: yields the next page from the specified API method
    """

    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("WAITING...")
            time.sleep(60)


def get_follower_ids(source_id):
    """
    gets Twitter user's followers

    :param source_id: the Twitter id of the source user
    :return: list of Twitter ids - followers of source user
    """

    num = 0
    followers = []
    for follower in limit_handled(tweepy.Cursor(api.followers_ids, id=source_id).items()):
        num += 1
        followers.append(follower)
    return followers


def get_following_ids(source_id):
    """
    gets users who Twitter user follows (following/friends)

    :param source_id: the Twitter id of the source user
    :return: list of Twitter ids - source user following list
    """

    num = 0
    following = []
    for following_user in limit_handled(tweepy.Cursor(api.friends_ids, id=source_id).items()):
        num += 1
        following.append(following_user)
    return following
