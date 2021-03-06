# -*- coding:utf-8 -*-

from math import sqrt
import time

"""
prefs : {人の名前:{アイテム名:評価}}
"""

# prefsを作成する関数
def create_prefs(userlist,ratings):
    # prefs
    prefs = {}
    for user in userlist:
        prefs.setdefault(user[0], {})

    for rate in ratings:
        prefs[rate[0]][rate[1]]=int(rate[2])

    return prefs

# 二人の人物の距離を基にした類似性スコアを返す
def sim_distance(prefs, person1, person2):
    sum_of_squares = 0

    # すべての差の平方を足し合わせる
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)
                       for item in prefs[person1] if item in prefs[person2]])

    # 両者ともに評価しているものが一つもなければ０を返す
    if sum_of_squares == 0:
        return 0
    else:
        return 1.0/(1+sum_of_squares)

# 二人の人物のピアソン相関係数を返す
def sim_pearson(prefs, person1, person2):
    # 両者が互いに評価しているアイテムのリストを取得
    n = 0
    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    pSum = 0
    for item in prefs[person1]:
        if item in prefs[person2]:
            n += 1
            sum1 += prefs[person1][item]
            sum2 += prefs[person2][item]
            sum1Sq += pow(prefs[person1][item],2)
            sum2Sq += pow(prefs[person2][item],2)
            pSum += prefs[person1][item] * prefs[person2][item]

    if n == 0:
        return 0

    # ピアソンによるスコアを計算する
    num = pSum - (sum1 * sum2/n) # 分子
    den = sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n)) # 分母
    if den == 0:
        return 0

    r = num/den

    return r

# 二人の人物のコサイン相関係数を返す
def sim_cosine(prefs, person1, person2):

    n = 0
    nSum = 0
    sum1 = 0
    sum2 = 0

    for item in prefs[person1]:
        if item in prefs[person2]:
            n += 1
            nSUm += prefs[person1][item] * prefs[person2][item]
            sum1 += prefs[person1][item]
            sum2 += prefs[person2][item]

    if n == 0:
        return 0

    pSum = sqrt(sum1 * sum2)

    return nSum/pSum

# ディクショナリからprefsからpersonにもっともマッチするものたちを返す
# 結果の数と類似性関数はオプションのパラメータ
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other),other)
              for other in prefs if other != person]
    # 高スコアがリストの最初に来るように並び替える
    scores.sort()
    scores.reverse()
    return scores[0:n]

# person以外の全ユーザーの評点の重み付け平均を使い、personへの推薦を算出する
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 自分自身とは比較しない
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        # 0以下のスコアを無視する
        if sim <= 0:
            continue

        for item in prefs[other]:
            # まだ見ていない映画の得点のみの算出
            if item not in prefs[person] or prefs[person][item] == 0:
                # 類似度 * スコア
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 類似度を合計
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # 正規化したリストを作る
    rankings = [(total/simSums[item], item) for item,total in totals.items()]

    # ソート済みのリストを作る
    rankings.sort()
    rankings.reverse()
    return rankings

# ユーザーごとのアイテムの評価配列をアイテムごとのユーザーの評価配列に変える
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # itemとpersonを入れ替える
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    """
    アイテムをキーとして持ち、それぞれのアイテムに似ている
    アイテムのリストを値として持つディクショナリを作る
    """
    result = {}

    # 嗜好の行列をアイテム中心な形に反転させる
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # 巨大なデータセット用にステータスを表示
        c += 1
        if c%100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        # このアイテムにもっとも似ているアイテムたちを探す
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores
    return result

def getRecommendadItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # このユーザーに評価されたアイテムたちをループする
    for (item, rating) in userRatings.items():

        # このアイテムに対してユーザーがすでに評価を行っていれば無視する
        if item2 in userRatings:
            continue

        # 評価と類似度を掛け合わせたものの合計で重みづけする
        scores.setdefault(item2,0)
        scores[item2] += similarity * rating

        # すべての類似度の合計
        totalSim.setdefault(item2, 0)
        totalSim[item2] += similarity

        # 正規化のため、それぞれの重み付けしたスコアを類似度の合計で測る
    rankings = [(score/totalSim[item], item) for item,score in scores.items()]

    # 降順に並べたランキングを返す
    rankings.sort()
    rankings.reverse()
    return rankings



if __name__ == "__main__":

    # movieID::title::genres
    movielist = []

    # userID::性別::年齢::職業::zip-code
    userlist = []

    # userID::movieID::rating::timestamp
    ratelist = []

    # 映画のデータ
    for line in open("../../data/ml-1m/movies.dat"):
        movielist.append(line.replace("\n","").split('::'))

    start = time.time()
    # ユーザーのデータ
    for line in open("../../data/ml-1m/users.dat"):
        userlist.append(line.replace("\n","").split('::'))

    # レーティングのデータ
    for line in open("../../data/ml-1m/ratings.dat"):
        ratelist.append(line.replace("\n","").split('::'))

    # prefsの作成
    prefs = {}
    prefs = create_prefs(userlist, ratelist)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
