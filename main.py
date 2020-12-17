#!/usr/bin/env python3

import urllib.request
#from requests_oauthlib import OAuth1Session
import datetime
import requests
import tweepy
from flask import Flask, render_template, request, jsonify, make_response, abort, send_from_directory
from flask_cors import CORS
import os
import urllib.parse
#認証情報と、その取得をkey.pyとして保存
import key



def remove_query(url):
    key = "tag"
    pr = urllib.parse.urlparse(url)
    d = urllib.parse.parse_qs(pr.query)
    d.pop(key, None)
    return urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))


def search_tweets(requestedSearchWord=""):
    #apiを取得
    auth = tweepy.OAuthHandler(key.getConsumerKey(), key.getConsumerSecret())
    auth.set_access_token(key.getAccessToken(), key.getAccessSecret())
    api = tweepy.API(auth)

    #検索キーワードを設定する この時に動画付きの条件・リツイートを除く条件を指定
    searchWord = requestedSearchWord +  " -filter:video exclude:retweets" 
    #searchWord = "2乗の和の幾何的"
    
    # twitter内を検索する
    result_json = {"statuses": [], "search_word": searchWord}

    #処理時間やリクエスト数の制限を考慮して上限を設定
    statuses = api.search(q=searchWord, lang='ja', result_type='recent', count=100, tweet_mode='extended')
    while True:
        
        if (len(statuses) == 0) or (len(result_json["statuses"]) > 180):
            break

        for i in range(len(statuses)):       
            if hasattr(statuses[i], 'extended_entities'):
                for media in statuses[i].extended_entities.get('media', [{}]):
                    if media.get('type', None) == 'video':
                        
                        #print("ユーザーID:" + statuses[i].user.name) #userIDを表示
                        #print("ユーザー名:" + statuses[i].user.screen_name) #ユーザー名を表示
                        #print("投稿日時:" + str(statuses[i].created_at + datetime.timedelta(hours=9))) #投稿日時を表示
                        #print(statuses[i].full_text) #ツイートを表示
                        
                        video_url = remove_query(media['video_info']['variants'][0]['url'])
                        #if (".mp4" in video_url) or (".m3u8" in video_url):
                        if (".mp4" in video_url):
                            
                            #print('video url: ' + video_url)
                            
                            result_json["statuses"].append({"user_name": statuses[i].user.name,
                                                        "user_id": statuses[i].user.screen_name,
                                                        "icon_url": statuses[i].user.profile_image_url,
                                                        "datetime": str(statuses[i].created_at + datetime.timedelta(hours=9)).replace('-', '/'),
                                                        "video_url": video_url,
                                                        "url": "https://twitter.com/" + statuses[i].user.screen_name + "/status/" + statuses[i].id_str,
                                                        "text": statuses[i].full_text                                                    
                                                        })
                            last_result = statuses[i].id_str
                            


                            #print()
        statuses = api.search(q=searchWord, lang='ja', result_type='recent', count=100, tweet_mode='extended', max_id=(int(last_result) - 1))
    """
    #動作テスト用に10件だけ検索する
    statuses = api.search(q=searchWord, lang='ja', result_type='recent', count=10, tweet_mode='extended')
    for i in range(len(statuses)):       
        if hasattr(statuses[i], 'extended_entities'):
            for media in statuses[i].extended_entities.get('media', [{}]):
                if media.get('type', None) == 'video':

                    video_url = remove_query(media['video_info']['variants'][0]['url'])
                    #if (".mp4" in video_url) or (".m3u8" in video_url):
                    if (".mp4" in video_url):
                        result_json["statuses"].append({"user_name": statuses[i].user.name,
                                                    "user_id": statuses[i].user.screen_name,
                                                    "icon_url": statuses[i].user.profile_image_url,
                                                    "datetime": str(statuses[i].created_at + datetime.timedelta(hours=9)).replace('-', '/'),
                                                    "video_url": video_url,
                                                    "url": "https://twitter.com/" + statuses[i].user.screen_name + "/status/" + statuses[i].id_str,
                                                    "text": statuses[i].full_text                                                    
                                                    })
    """                                                
    
    return result_json
                        

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

@app.route('/')
def search():
    return render_template('search.html', title='twimovie player')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')

@app.route('/static/img/skip.svg')
def skip_svg():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'skip.svg')


@app.route('/get', methods=['GET'])  # Getだけ受け付ける
def get():  # 関数名は重複していなければなんでもよい
    result = search_tweets(got_search_word)
    return jsonify(result)

@app.route('/post', methods=['POST'])  # Postだけ受け付ける
def post():
    global got_search_word
    got_search_word = request.form["word"]  # Postで送ったときのパラメータの名前を指定する

    

    return make_response(got_search_word)

if __name__=='__main__':
    app.run(debug=True)


"""
参考
https://qiita.com/KEI_y/items/2d4d32c78f88fdb16eee
https://thinkami.hatenablog.com/entry/2017/11/02/062226
"""
