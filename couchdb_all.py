#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author : Henry
Date   : 2019.5.14
Version: 1.0
Description:

"""
import json
import couchdb

COUCHDB_SERVER = "http://admin:password@172.26.37.226:5984"
DB_SCORE_NAME = "db_score"
DB_LOCATION_NAME = "db_location"

FILE_SCORE_PATH = "all_tweets_of_users.json"
FILE_LOCATION_PATH = "user_AU.json"

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


if __name__ == "__main__":
    # set_db_score(FILE_SCORE_PATH)
    # set_db_location(FILE_LOCATION_PATH)
    #
    # tweet_score = {"time": "2019-05-13 13:14:05", "user_id": 406184685, "tweet_id": 1127924977510969349, "text": "Think the #giro might be using Google Translate this year. \u2018Also for want of a roof\u2019 ?????? #couchpeloton", "Sloth:": 0.3094}
    # add_db_score(tweet_score)
    # tweet_location = {"time": "Mon May 13 13:14:05 +0000 2019", "user_id": 406184685, "place": "Melbourne, Victoria", "coordinate": [145.053135344, -37.972566514250005], "polygon": "20803"}
    # add_db_location(tweet_location)
    #
    # tweet_location = {"time": "Mon May 13 13:14:05 +0000 2019", "user_id": 406184685, "place": "MK", "coordinate": [145., -37.], "polygon": "2"}
    # update_db_location(tweet_location)
    #
    # tweet_location_1 = {"time": "Mon May 13 13:14:05 +0000 2019", "user_id": 406184685, "place": "MK", "coordinate": [145., -37.], "polygon": "2"}
    # tweet_location_2 = {"time": "Mon May 13 13:14:05 +0000 2019", "user_id": 40618468, "place": "MK", "coordinate": [145., -37.], "polygon": "2"}
    # user_is_exist_1 = query_db_location_by_user_id(tweet_location_1)
    # user_is_exist_2 = query_db_location_by_user_id(tweet_location_2)
    # print(user_is_exist_1, user_is_exist_2)

    db_score_to_json()
    db_location_to_json()

