import tweepy
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import sys
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import couchdb
# -------------------
COUCHDB_SERVER = "http://admin:password@172.26.37.226:5984"
DB_SCORE_NAME = "db_score"
DB_LOCATION_NAME = "db_location"

# FILE_SCORE_PATH = "all_tweets_of_users.json"
# FILE_LOCATION_PATH = "user_AU.json"

DOC_QUERY_SCORE = {'_id': '_design/query_score',
                 'views': {
                     '_id': {
                         'map': 'function(doc){emit(doc._id,doc)};'
                     },
                     'user_id': {
                         'map': 'function(doc){emit(doc.user_id,doc)};'
                     },
                     'tweet_id': {
                         'map': 'function(doc){emit(doc.tweet_id,doc)};'
                     },
                     'text': {
                         'map': 'function(doc){emit(doc.text,doc)};'
                     }
                 }
                 }
DOC_QUERY_LOCATION = {'_id': '_design/query_location',
                 'views': {
                     '_id': {
                         'map': 'function(doc){emit(doc._id,doc)};'
                     },
                     'user_id': {
                         'map': 'function(doc){emit(doc.user_id,doc)};'
                     },
                     'location': {
                         'map': 'function(doc){emit(doc.location,doc)};'
                     }
                 }
                 }


def get_db(db_name, query_name):
    server = couchdb.Server(COUCHDB_SERVER)
    try:
        _db = server.create(db_name)
        _db.save(query_name)
    except:
        _db = server[db_name]

    return _db

def set_db_score(file_score_path):
    file_score = open(file_score_path)
    docs_score = []
    for i, _tweet in enumerate(file_score):
        json_tweet = json.loads(_tweet)
        doc = dict(time=json_tweet['time'], user_id=json_tweet['user_id'],
                   tweet_id=json_tweet['tweet_id'], text=json_tweet['text'], sloth=json_tweet['Sloth:']) #####
        docs_score.append(doc)

    db_score = get_db(DB_SCORE_NAME, DOC_QUERY_SCORE)
    db_score.update(docs_score)

def add_db_score(tweet_score):
    doc_score = [dict(time=tweet_score['time'], user_id=tweet_score['user_id'],
                      tweet_id=tweet_score['tweet_id'], text=tweet_score['text'], sloth=tweet_score['Sloth:'])]
    db_score = get_db(DB_SCORE_NAME, DOC_QUERY_SCORE)
    db_score.update(doc_score)

def set_db_location(file_location_path):
    file_location = open(file_location_path)
    docs_location = []
    for i, _tweet in enumerate(file_location):
        json_tweet = json.loads(_tweet)
        doc = dict(time=json_tweet['time'], user_id=json_tweet['user_id'], place=json_tweet['place'],
                   coordinate=json_tweet['coordinate'], polygon=json_tweet['polygon'])
        docs_location.append(doc)

    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)
    db_location.update(docs_location)

def add_db_location(tweet_location):
    doc_location = [dict(time=tweet_location['time'], user_id=tweet_location['user_id'], place=tweet_location['place'],
                         coordinate=tweet_location['coordinate'], polygon=tweet_location['polygon'])]

    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)
    db_location.update(doc_location)

def update_db_location(tweet_location):
    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)
    result_user_id = db_location.view('query_location/user_id', keys=[tweet_location['user_id']])
    result_user_id_tweet = result_user_id.rows[0].value
    doc_location = [dict(
        _id=result_user_id_tweet['_id'],
        _rev=result_user_id_tweet['_rev'],
        time=tweet_location['time'],
        user_id=tweet_location['user_id'],
        place=tweet_location['place'],
        coordinate=tweet_location['coordinate'],
        polygon=tweet_location['polygon']
    )]
    db_location.update(doc_location)

def query_db_location_by_user_id(tweet_location):
    user_is_exist = False
    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)
    result_user_id = db_location.view('query_location/user_id', keys=[tweet_location['user_id']])
    if len(result_user_id.rows) > 0:
        user_is_exist = True

    return user_is_exist

def db_score_to_json():
    file_score = open('score.json', 'a')

    db_score = get_db(DB_SCORE_NAME, DOC_QUERY_SCORE)

    list_id = list()
    for _id in db_score:
        list_id.append(_id)

    result_db_score = db_score.view('query_score/_id', keys=list_id[:-1])
    for row in result_db_score:
        data = row.value
        json.dump(data, file_score)
        file_score.write('\n')
        file_score.flush()

def db_location_to_json():
    file_location = open('location.json', 'a')

    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)

    list_id = list()
    for _id in db_location:
        list_id.append(_id)

    result_db_location = db_location.view('query_location/_id', keys=list_id[:-1])
    for row in result_db_location:
        data = row.value
        json.dump(data, file_location)
        file_location.write('\n')
        file_location.flush()






# -------------------------------------
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

true_num = 0
false_num = 0

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

        if (query_db_location_by_user_id(data)):
            update_db_location(data)
        else:
            add_db_location(data)
            # print('true')
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
                    'text': str(tweet.full_text), 'Sloth:': scoringText(str(tweet.full_text), [])}
            # print('uploadtweet')
            add_db_score(data)

    # print('# of tweets of ' , user_id, ' : ', len(data_list))
    # print('Send to DB')


def GetTwitterListen():
    coordinate_area = [float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])]
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(languages=['en'], locations=coordinate_area)

main()