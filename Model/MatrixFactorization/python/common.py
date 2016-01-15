# -*- coding:utf-8 -*-

import pandas as pd
import math
import random

def create_ratings():
    
    userlist = create_element("../../../data/ml-1m/users.dat")
    itemlist = create_element("../../../data/ml-1m/movies.dat")
    # userID::movieID::rating::timestamp
    ratelist = create_ratelist("../../../data/ml-1m/ratings.dat")
    prefs = create_prefs(userlist, ratelist)
    rate_matrix = {}
    for user in userlist:
        rate_matrix.setdefault(user, {})
        for item in itemlist:
            if prefs[user].has_key(item):
                rate_matrix[user][item] = prefs[user][item]
            else:
                rate_matrix[user][item] = 0

    return rate_matrix

def create_prefs(userlist, ratings):
    
    # prefs
    prefs = {}
    for user in userlist:
        prefs.setdefault(user, {})

    for rate in ratings:
        prefs[int(rate[0])-1][int(rate[1])-1]=int(rate[2])

    return prefs

def create_element(filename):

    ret = []
    maxElement = 0
    for line in open(filename):
        now_element = int(line.replace("\n","").split('::')[0])
        maxElement = now_element if now_element > maxElement else maxElement

    for i in range(maxElement):
        ret.append(i)
    
    return ret

def create_ratelist(filename):

    ret = []

    for line in open(filename):
        ret.append(line.replace("\n","").split('::'))

    return ret

"""
テストデータを300個作る
@param(RateArray) キーにユーザーとアイテムを持つ二次元ディクショナリ
@return(RateArray) テストデータを除いた教師データ
@return(testData) キーにユーザーとアイテムを持つ300個のテスト用データディクショナリ
"""
def create_test_data(RateArray):
  
  testData = {}
  count = 0
  while(count < 300):
      user = random.choice(RateArray.keys())
      item = random.choice(RateArray[user].keys())
      if RateArray[user][item] == 0:
          continue
      if testData.has_key(user):
          continue
      testData.setdefault(user, {})
      count+=1
      testData[user][item] = RateArray[user][item]
      RateArray[user][item] = 0

  return RateArray, testData

