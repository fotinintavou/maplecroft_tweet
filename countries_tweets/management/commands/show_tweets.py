from django.core.management.base import BaseCommand

from countries_tweets.models import Tweets

class Command(BaseCommand):
    help = 'Show the current tweets saved in db - for debugging purpose'

    def handle(self, *args, **options):
        print Tweets.objects.get_latest_tweets()
        for tweet in Tweets.objects.all():
            print "*************************"
            print tweet.published_at
            print tweet.contents