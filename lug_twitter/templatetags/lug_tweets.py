from django import template

import tweepy

register = template.Library()

# This function accepts a list of users and the desired number of tweets
# to return. It returns a list of objects that have the simple
class SimpleTweet(object):
    def __init__(self, tweet):
        self.text = tweet.text
        self.user = tweet.author.screen_name
        self.user_pic = str(tweet.author.profile_image_url)
        check = self.user_pic.split('.')
        self.timestamp = str(tweet.created_at)
        
        # Make sure that we're getting an integer.
        self.link = "http://about:blank"
        if type(tweet.id) is int:
            self.link = 'https://twitter.com/isharacomix/status/%d' % (tweet.id)
        
        # This makes sure that nobody has hijacked the twitter API and sends
        # us naughty things.
        if not (len(check) > 2 and check[1] == 'twimg' and check[2].startswith("com/")):
            self.user_pic = ""


def get_tweets(owner, slug, total):
    report = []
    # This try-catch makes it so when twitter goes down, it doesn't take our
    # site with it.
    try:
        raw_tweets = tweepy.api.list_timeline(owner, slug) + tweepy.api.user_timeline(owner)
        raw_tweets.sort(lambda x, y: cmp(y.created_at, x.created_at))
        for t in raw_tweets[:total]:
            report.append( SimpleTweet(t) )
    except tweepy.TweepError:
        pass
    return report


@register.inclusion_tag('lug_twitter/tweets.html')
def tweets(total):
    return {'tweets': get_tweets("ncsulug", "people-ncsulug", total)}

