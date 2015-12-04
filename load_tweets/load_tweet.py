import sys

__author__ = 'anton'

from twitter_auth import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
import time
import csv

try:
    import twitter
except ImportError:
    print("""\
You need to ...
    pip install twitter
If pip is not found you might have to install it using easy_install.
If it does not work on your system, you might want to follow instructions
at https://github.com/sixohsix/twitter, most likely:
  $ git clone https://github.com/sixohsix/twitter
  $ cd twitter
  $ sudo python setup.py install
""")
    sys.exit(1)


class TwitterAuth:
    def __init__(self):
        self.api = twitter.Twitter(auth=twitter.OAuth(consumer_key=CONSUMER_KEY,
                                                      consumer_secret=CONSUMER_SECRET,
                                                      token=ACCESS_TOKEN_KEY,
                                                      token_secret=ACCESS_TOKEN_SECRET))

    def home_timeline(self, path):
        time_line = self.api.statuses.home_timeline()
        response = []
        response.append(['TweetId', 'TweetText'])
        for post in time_line:
            if post['lang'] != 'en':
                continue
            response.append([post['id'], post['text'].encode('utf-8')])

        if len(response) > 0:
            self.writeToCsvFile(path, response)
            print("TimeLine loaded to {0}".format(path))

    def writeToCsvFile(self, path, data):
        with open(path, 'w') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerows(data)

    def download_tweet(self, tweet_id):
        try:
            response = self.api.statuses.show(_id=tweet_id)
            if response.rate_limit_remaining <= 0:
                self.twitter_delay(response.rate_limit_reset)
        except twitter.TwitterError as e:
            self.handle_twitter_error(e, tweet_id)

    def twitter_delay(self, rate_limit_reset):
        wait_seconds = rate_limit_reset - time.time()
        print("Rate limiting requests us to wait %f seconds" % wait_seconds)
        time.twitter_delay(wait_seconds + 5)

    def handle_twitter_error(self, error, tweet_id):
        fatal = True
        for m in error.response_data['errors']:
            fatal, message = self.get_error_message(m['code'], tweet_id)
            print(message)

        if fatal:
            raise

    @staticmethod
    def get_error_message(code, twitter_id):
        fatal = True
        message = ""
        if code == 34:
            message = "Tweet missing: {0}".format(twitter_id)
            fatal = False
        elif code == 63:
            message = "User of tweet '{0}' has been suspended.".format(twitter_id)
            fatal = False
        elif code == 88:
            message = "Rate limit exceeded."
            fatal = True
        elif code == 179:
            message = "Not authorized to view this tweet."
            fatal = False
        elif code == 144:
            message = "No status found"
            fatal = False
        return fatal, message


def main():
    twitter_auth = TwitterAuth()
    twitter_auth.home_timeline("../timeline.csv")


if __name__ == '__main__':
    main()
