# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TweetManager(models.Manager):

    def get_latest_tweets(self, offset=0, limit=10):
        return self.all().order_by('published_at')[offset:limit]

    def remove_all(self):
        self.all().delete()


class Tweets(models.Model):
    """
    Save imported tweets to the database
    """
    contents = models.TextField(u"Maplecroft Tweet Content", default='no_tweet_available')
    country_lat = models.TextField(u"Country Latitude", default="")
    country_lon = models.TextField(u"Country Longtitude", default="")
    published_at = models.DateTimeField(u"Published At")
    updated_at = models.DateTimeField(u"Last Update", auto_now=True)
    created_at = models.DateTimeField(u"Date", auto_now_add=True)

    objects = TweetManager()

    class Meta:
        verbose_name = 'Maplecroft Tweet'
        verbose_name_plural = 'Maplecroft Tweets'

    def __unicode__(self):
        return self.contents