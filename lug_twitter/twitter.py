# -*- coding: utf-8 -*-

import tweepy
from django.utils.timezone import make_aware, utc

class SimpleTweet(object):
    def __init__(self, tweet):
        self.text = tweet.text
        self.user = tweet.author.screen_name
        self.user_pic = str(tweet.author.profile_image_url)
        check = self.user_pic.split('.')
        print tweet.created_at
        self.timestamp = make_aware(tweet.created_at, utc)

        # Make sure that we're getting an integer.
        self.link = "#"
        if type(tweet.id) is int:
            self.link = 'https://twitter.com/%s/status/%d' % (self.user,
                                                              tweet.id)

        # This makes sure that nobody has hijacked the twitter API and sends
        # us naughty things.
        check = self.user_pic.split('.')
        if not (len(check) > 2 and check[1] == 'twimg' and check[2].startswith("com/")):
            self.user_pic = ""


def get_tweets(owner, slug, total):
    """
    Retrieves the tweets from a Twitter user and one of their lists.

    :param owner: The username of the list's owner.
    :param slug: The slug of the list.
    :param total: The number of tweets to return.
    :return: A list of `SimpleTweet` objects.
    """
    # This try-catch makes it so when twitter goes down, it doesn't take our
    # site with it.
    try:
        raw_tweets = (tweepy.api.list_timeline(owner, slug) +
                      tweepy.api.user_timeline(owner))
        raw_tweets.sort(key=lambda t: t.created_at, reverse=True)
        return [SimpleTweet(t) for t in raw_tweets[:total]]
    except tweepy.TweepError:
        return []
