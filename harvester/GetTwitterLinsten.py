import tweepy
import json
import sys
# key and secret.
consumer_key = 'LzOxVuyHgGu9QP4b8skZxUVvS'
consumer_secret = 'nbLuOAibNpCiiLfgsMwKTPiV4PYNhTK21ddWli40T3dI08YgY4'
access_token = '1120218841278115840-6CgqMItD1yLdo1ejbnhfgNfIBz5upA'
access_token_secret = 'TqcBGcTzgNKkkLipAw3wmHek8iTg8bM7vwirfL7wYT23t'


# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth)



# get the latest tweet in Au.

outfile = open('latest_tweets.json', 'a')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        json_str = status._json
        coordinates = [json_str['place']['bounding_box']['coordinates'][0][0],
                       json_str['place']['bounding_box']['coordinates'][0][2]]
        x1 = coordinates[0][0]
        x2 = coordinates[1][0]
        y1 = coordinates[0][1]
        y2 = coordinates[1][1]
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        id = json_str['user']['id']
        place = json_str['place']['full_name']
        data = {'time': json_str['created_at'], 'user_id': id, 'place': place, 'coordinate': [x, y]}
        print(data)
        json.dump(data, outfile)
        outfile.write('\n')
        outfile.flush()

# coordinate_au=[112.921114, -43.740482, 159.109219, -9.142176]

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(languages =['en'], locations=[112.921114, -43.740482, 159.109219, -9.142176])
