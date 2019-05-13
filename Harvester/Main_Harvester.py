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


def main():
    id_list = search_user_from_old_tweets()
    search_tweets_from_user_list(id_list)
    GetTwitterLinsten()
def search_user_from_old_tweets():
    id_list = []
    # -----------------------------------------------------------------------
    # search all tweets 6-9 days ago, and only record the data from first tweet per user.
    # The data includes timpestamp, user id, full_name of the place, southwest and northeast points of the bounding box.
    # It will keep the id list for further use.
    places = api.geo_search(query="Australia", granularity='country')
    place_id = places[0].id
    place_val = "place:%s" % place_id
    outfile = open('user_AU.json', 'w')
    for page in tweepy.Cursor(api.search, q=place_val, count=9999).pages():
        try:
            for t in page:
                json_str = t._json
                id = json_str['user']['id']
                coordinates = [json_str['place']['bounding_box']['coordinates'][0][0],
                               json_str['place']['bounding_box']['coordinates'][0][2]]
                x1 = coordinates[0][0]
                x2 = coordinates[1][0]
                y1 = coordinates[0][1]
                y2 = coordinates[1][1]
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                polygon = find_sa3(float(x), float(y))
                if id not in id_list and polygon is not None:
                    place = json_str['place']['full_name']
                    data = {'time': json_str['created_at'], 'user_id': id, 'place': place, 'coordinate': [x, y],
                            'polygon': polygon}
                    # print(data)
                    id_list.append(id)
                    # print(data)
                    # idfile.write(str(id))
                    # idfile.write('\n')
                    # idfile.flush()
                    json.dump(data, outfile)
                    outfile.write('\n')
                    outfile.flush()
            # print('Total processed tweets: ', tweets_num, 'Total unique id:', len(id_list))
            if len(id_list) > int(sys.argv[6]):
                break
        except tweepy.RateLimitError as e:
            print(e)
    return id_list



def search_tweets_from_user_list(id_list):
    # search old tweets of users from above searching.
    index_input = int(sys.argv[5])
    file_name = 'send_data'+ str(index_input)+'.json'
    file = open(file_name , 'w', buffering= 50)
    # total_tweet_num = 0
    # print('start search tweets')
    # data_list = []
    tweet_num = 0

    for index in range(index_input-int(sys.argv[6])/4, index_input):
        for page in tweepy.Cursor(api.user_timeline, id=id_list[index], tweet_mode='extended', lan='en',
                                  count=200).pages(1):
            for tweet in page:
                tweet_num += 1
                json_str = tweet._json
                data = {'time': str(tweet.created_at), 'user_id': id_list[index], 'tweet_id': json_str['id'],
                        'text': str(tweet.full_text), 'Sloth:': scoringText(str(tweet.full_text), [])}
                # print(data)
                json.dump(data, file)
                file.write('\n')
                file.flush()

                # if tweet_num == 5000:
                #     tweet_num = 0
                #     # send file to database, print('Empty file')
                #     # clear the file
                #     file.truncate(0)
        # total_tweet_num += tweet_num
        # print(id_val, ' Tweets num:', tweet_num)
    # print('Total tweets:', total_tweet_num)


main()