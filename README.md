# maplecroft_tweet

A basic application which:
- displays the 10 latest tweets from Verisk Maplecroft
- pinpoints to a google map the countries referenced in these tweets 
- displays the tweets if one hovers over the pinpointed countries

This application is based on the Django framework. JavaScript was also used, as well as google api and twitter api.

## Installation

**Python version:** 2.7.1

**Django version:** 1.11.5

**Install modules :**  pip install tweepy pandas

**Install the app:** 

Perform the following commands:

- git clone https://github.com/fotinintavou/maplecroft_tweet.git
- cd maplecroft_tweet/
- python manage.py migrate
- python manage.py runserver
- Follow the link to the webpage

## Using the app

### 1. countries_tweets

#### models.py

The app has one model: Tweets and one model manager: TweetManager. 

Tweets objects have the following fields:

Field Name | Description
------------ | -------------
contents | The text content of each tweet
country_lat | The related country's latitude
country_lon | The related country's longtitude
published_at | The day it was published (easy for sorting)
updated_at | The day it was last updated
created_at | The day it was created

#### import_tweets.py

This has the class ImportTweets, which contains methods for:
- parsing the countries.csv file (see below)
- finding the countries inside a tweet
- fetching the tweets from twitter
- updating the Tweets model

#### countries.csv

The csv file which is parsed in import_tweets.py. Contains all countries with their respective map coordinates.

#### views.py

Currently there is only one index page. When index method is called:

- Tweets are updated
- Latest 10 tweets are displayed. You can change this by inserting a different number here: latest_tweets_list = Tweets.objects.order_by("-published_at")[:10]
- HTML template is loading

### 2. countries_tweets/management/commands 

Run the following command lines to test your app (twitter crdentials, tweets fetching, etc):

- python manage.py update_tweets

- python manage.py show_tweets

### 3. maplecroft_tweets

#### settings.py

Contains base dir, template dirs, twitter credentials

#### urls.py

Calls views' index method

### 4. templates

#### tweets.html

HTML code for the index page. 

Loads the map from the google api (need to give a key).
Django variables (tweet text, longtitude, latitude) are pushed to JavaScript variables and then displayed on the map.

#### tweets.css

Very basic css to divide the page in 3 containers:

- One for the tweets
- One for the map
- Footer
