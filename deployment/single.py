#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author : Henry
Date   : 2019.5.10
Version: 1.0
Description:

"""
import json
import pickle
import couchdb

COUCHDB_SERVER = "http://127.0.0.1:5984"
DB_SCORE_NAME = 'db_score'
DB_LOCATION_NAME = 'db_location'
FILE_SCORE_PATH = "all_tweets_of_users.json"
FILE_LOCATION_PATH = "latest_tweets.json"
DOC_QUERY_SCORE = {'_id': '_design/query_score',
                 'views': {
                     'dict_id': {
                         'map': 'function(doc){emit(doc.dict_id,doc)};'
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
                     'dict_id': {
                         'map': 'function(doc){emit(doc.dict_id,doc)};'
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


def predict_score(text):
    # the function of predicting score
    score_1 = 0
    score_2 = 0

    return score_1, score_2


def set_db_score(file_score_path):
    file_score = open(file_score_path)
    # json_score = json.load(file_score)
    json_score = file_score
    docs_score = []
    for i, _tweet in enumerate(json_score):
        tweet_list = _tweet.split(',')
        text = tweet_list[3][:-2]
        score_1, score_2 = predict_score(text)
        doc = dict(dict_id=i+1, time=tweet_list[0][1:], user_id=tweet_list[1],
                   tweet_id=tweet_list[2], text=text, score_1=score_1, score_2=score_2)
        docs_score.append(doc)

    db_score = get_db(DB_SCORE_NAME, DOC_QUERY_SCORE)
    db_score.update(docs_score)


def set_db_location(file_location_path):
    file_location = open(file_location_path)
    # json_location = json.load(file_location)
    json_location = file_location
    docs_location = []
    for i, _tweet in enumerate(json_location):
        tweet_list = _tweet.split(',')
        tweet_length = len(tweet_list)

        time = tweet_list[0][1:]
        user_id = tweet_list[1]
        location = tweet_list[2]
        area_num = tweet_list[3][:-2]
        if tweet_length > 4:
            location = tweet_list[2:-1]
            print(location)
            area_num = tweet_list[-1][:-2]

        doc = dict(dict_id=i + 1, time=time, user_id=user_id,
                   location=location, area_num=area_num)
        docs_location.append(doc)

    db_location = get_db(DB_LOCATION_NAME, DOC_QUERY_LOCATION)
    db_location.update(docs_location)


def update_db_score_user_id(tweet_list):
    return


def update_db_score_tweet_id(tweet_list):
    return


def query_db_score(_tweet):
    tweet_list = _tweet.split(',')
    user_id = tweet_list[1]
    tweet_id = tweet_list[2]

    db_score = get_db(DB_SCORE_NAME, DOC_QUERY_SCORE)
    result_user_id = db_score.view('query/user_id', keys=user_id)
    result_tweet_id = db_score.view('query/tweet_id', keys=tweet_id)

    if result_user_id is None:
        update_db_score_user_id(tweet_list)
    elif result_tweet_id is None:
        update_db_score_tweet_id(tweet_list)


if __name__ == "__main__":
    # set_db_score(FILE_SCORE_PATH)
    # set_db_location(FILE_LOCATION_PATH)
    tweet = ""
    query_db_score(tweet)

