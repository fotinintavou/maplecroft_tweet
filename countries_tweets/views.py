# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse

from .models import Tweets
import import_tweets

# Create your views here.
def index(request):

    importer = import_tweets.ImportTweets()
    importer.update_tweets()
    latest_tweets_list = Tweets.objects.order_by("-published_at")[:10]
    template = loader.get_template('tweets.html')
    context = {
        'latest_tweets_list': latest_tweets_list
    }
    return HttpResponse(template.render(context, request))