from django.core.management.base import BaseCommand

from countries_tweets.import_tweets import ImportTweets


class Command(BaseCommand):
    help = 'Import Tweets'

    def handle(self, *args, **options):
        importer = ImportTweets()
        importer.update_tweets()