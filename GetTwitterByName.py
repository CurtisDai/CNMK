import tweepy
import json
import sys
import ast
# key and secret.
consumer_key = 'LzOxVuyHgGu9QP4b8skZxUVvS'
consumer_secret = 'nbLuOAibNpCiiLfgsMwKTPiV4PYNhTK21ddWli40T3dI08YgY4'
access_token = '1120218841278115840-6CgqMItD1yLdo1ejbnhfgNfIBz5upA'
access_token_secret = 'TqcBGcTzgNKkkLipAw3wmHek8iTg8bM7vwirfL7wYT23t'

# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
id_list = []

#command input: id
# id_value = int(sys.argv[1])
# file_name = sys.argv[1]
# file_name += '.json'

# with open('file_name','r',encoding="utf8") as f:
#     mylist = ast.literal_eval(f.read())
#     for item in mylist:
#         id_list.append(item[3])
# print (id_list)

with open('id_list_v5.txt', 'r') as f:
    id_list += f.read().splitlines()

file = open('tweets_from_id_v3.json', 'a')

json_list = []
tweet_num = 0

for id_val in id_list:
    tweet_num = 0
    tweet_loc_not_null = 0
    try:
        for page in tweepy.Cursor(api.user_timeline, id=id_val, tweet_mode='extended', count=9999).pages():
            for tweet in page:
                tweet_num += 1
                data = {'time': str(tweet.created_at), 'user_id': tweet.user.id, 'text': str(tweet.full_text),  'coordinates': tweet.coordinates}
                json.dump(data, file)
                file.write('\n')
    except :
            pass
   # print(tweet_num, tweet_loc_not_null)
    print(tweet_num)

# with open(file_name, 'w') as outfile:
#    json.dump(json_list, outfile, indent=4)

