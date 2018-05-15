import re
import tweepy
import pandas

from django.conf import settings
from django.db import transaction
from countries_tweets.models import Tweets


class ImportTweets:

    def __init__(self):

        self.consumer_key = settings.TWITTER_FEED_CONSUMER_PUBLIC_KEY
        self.consumer_secret = settings.TWITTER_FEED_CONSUMER_SECRET
        self.o_auth_token = settings.TWITTER_FEED_OPEN_AUTH_TOKEN
        self.o_auth_secret = settings.TWITTER_FEED_OPEN_AUTH_SECRET

    def update_tweets(self):
        raw_tweets = self._get_latest_tweets_from_api()
        tweets = [self._tweepy_status_to_tweet(status=status) for status in raw_tweets]
        self._replace_all_tweets(tweets)


    def _get_latest_tweets_from_api(self):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.o_auth_token, self.o_auth_secret)
        api = tweepy.API(auth)
        return api.user_timeline(screen_name = 'MaplecroftRisk')

    def _tweepy_status_to_tweet(self, status):
        """
        Fields documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
        """
        tweet = Tweets()
        tweet.published_at = status.created_at
        tweet.contents = status.text
        tweet.country_lat, tweet.country_lon = self._find_countries_in_tweets(status.text)
        return tweet

    def _find_countries_in_tweets(self, tweet_content):

        tweet_in_list = []
        tweet_in_list.append(re.findall('[A-Za-z\']+(?:\`[A-Za-z]+)?', tweet_content))

        countries, abbreviations, countries_lat_long_dict, abbreviations_lat_long_dict = self._parse_csv_countries_file()

        for tw in range(len(tweet_in_list[0])):
            if tweet_in_list[0][tw] in countries:
                return countries_lat_long_dict[tweet_in_list[0][tw]][0], countries_lat_long_dict[tweet_in_list[0][tw]][1]

        return 0, 0

    def _parse_csv_countries_file(self):

        countries_lat_long_dict = {}
        abbreviations_lat_long_dict = {}
        colnames = ['country', 'abbrev',  'longitude', 'latitude']
        data = pandas.read_csv('countries_tweets/countries.csv', names=colnames)

        countries = data.country.tolist()
        abbreviations = data.abbrev.tolist()
        latitude = data.latitude.tolist()
        longitude = data.longitude.tolist()

        for count in range(len(countries)):
            countries_lat_long_dict[countries[count]] = [latitude[count], longitude[count]]
            abbreviations_lat_long_dict[abbreviations[count]] = [latitude[count], longitude[count]]

        return countries, abbreviations, countries_lat_long_dict, abbreviations_lat_long_dict


    @transaction.atomic()
    def _replace_all_tweets(self, new_tweets):
        try:
            with transaction.atomic():
                Tweets.objects.remove_all()

                for tweet in new_tweets:
                    tweet.save()

            transaction.commit()
        except Exception:
            pass