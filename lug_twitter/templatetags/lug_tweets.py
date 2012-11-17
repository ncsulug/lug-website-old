# -*- coding: utf-8 -*-

from django import template
from django.core.cache import cache
from ..twitter import get_tweets

register = template.Library()

@register.inclusion_tag('lug_twitter/tweets.html')
def tweets(total):
    key = 'lug_twitter_timeline'

    tweets = cache.get(key)
    if tweets is None:
        tweets = get_tweets("ncsulug", "people-ncsulug", total)
        cache.set(key, tweets)
    return {'tweets': tweets}
