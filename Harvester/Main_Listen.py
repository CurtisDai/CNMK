import tweepy
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import sys
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

# key and secret.
consumer_key = str(sys.argv[1])
consumer_secret = str(sys.argv[2])
access_token = str(sys.argv[3])
access_token_secret = str(sys.argv[4])

# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def getRelevantWord(words):
    work_word_list=[]
    for word in words:
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                 work_word_list.append(lemma.name())
    return set(work_word_list)

def scoringText(text,word):
    wordset = getRelevantWord(word) if len(word)!= 0 else " "
    lemmatizer = WordNetLemmatizer()
    score = 0
    text_lem = " ".join([lemmatizer.lemmatize(t) for t in text.split()])
    if len([i for i in wordset if text_lem.find(i)!=-1])!=0:
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(text)['compound']
        #print(sid.polarity_scores(text))\n",
    return score

# print(scoringText("This isn't a shit study",["study","work"]))

with open('SA3_2016_AUST_small.json') as f:
    data = json.load(f)

dictPoly = {}
for d in data['features']:
    if 'geometry' in d and d['geometry']!= None:
        listP = d['geometry']['coordinates'][0]
        dictPoly[d['properties']['SA3_CODE16']] = listP if len(listP)>1 else listP[0]

def getSA3(lon,lat, polygon): #149.57900670400008, -35.5
    polygon = Polygon(polygon) # create polygon
    point = Point(lon, lat) # create point
    return(point.within(polygon))

def find_sa3(lon,lat):
    try:
        for poly in dictPoly:
            if getSA3(lon, lat, dictPoly[poly]):
                return poly
    except Exception as e:
        print(lon, lat)


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
        polygon = find_sa3(float(x), float(y))
        data = {'time': json_str['created_at'], 'user_id': id, 'place': place, 'coordinate': [x, y], 'polygon': polygon}
        # print(data)

        # query and send data to DB and update user
        # if (new user):
        #   GetTweetsFromAUser(user.id)
        GetTweetsFromAUser(id)
        # json.dump(data, outfile)
        # outfile.write('\n')
        # outfile.flush()


def main():
    GetTwitterListen()

def GetTweetsFromAUser(user_id):
    data_list = []
    for page in tweepy.Cursor(api.user_timeline, id=user_id, tweet_mode='extended', lan='en', count=9999).pages():
        tweet_num = 0
        for tweet in page:
            tweet_num += 1
            json_str = tweet._json
            data = {'time': str(tweet.created_at), 'user_id': user_id, 'tweet_id': json_str['id'],
                    'text': str(tweet.full_text)}
            data_list.append(data)

    print('# of tweets of ' , user_id, ' : ', len(data_list))
    print('Send to DB')

def GetTwitterListen():
    coordinate_area = [float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])]
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(languages=['en'], locations=coordinate_area)

main()