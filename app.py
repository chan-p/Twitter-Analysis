#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from jinja2 import Environment, FileSystemLoader
from flask import render_template
from flask import request, redirect, url_for
import sys
import tweepy
import MeCab
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy as sp
sys.path.append("/Library/Python/2.7/site-packages")

app = Flask(__name__)
app.config['DEBUG'] = True

# auth = tweepy.OAuthHandler('SjT3DTgX44ZCfLpk8cs7Joncb','IeIk6PYvhkDLIJd7cQp8ZV6mLSQuLS76jQOphCFo2TWPF6K60d')
##Local Version
auth = tweepy.OAuthHandler('wUPAJgKmupzKL5Y97vKeMuCGA','ApxmVcuJLRluNjL3I5cCxQk9hNfNgE5pHYivZnnHzzNDcHT9sb')
mt = MeCab.Tagger("mecabrc")


@app.route('/')
def Top():
    return render_template("Top.html",url=auth.get_authorization_url())


@app.route('/mainpage')
def mainpage():
    api = __get_API()

    textl = []
    stop_words = __get_stopwords()
    for tweet in tweepy.Cursor(api.user_timeline, id=__get_username(api)).items(150):
        res = mt.parseToNode(str(tweet.text.encode("utf-8")))
        while res:
            feat = res.feature.split(",")
            if (feat[0] == "名詞" or feat[0] == "形容詞" or feat[0] == "副詞") and (res.surface.isalpha() == False) and (res.surface.isdigit() == False) and (res.surface not in stop_words):
                textl.append(feat[6])
            res = res.next

    wc = create_wordcloud(" ".join(textl).decode("utf-8"))
    plt.figure(figsize=(13,16))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig("/Users/TomonotiHayshi/GitHub/Python/App/Wordcloud/system/static/cloud.jpg", bbox_inches='tight', pad_inches=0.0)
    # imgar = nd[y: y+h, x: x+w]
    # sp.misc.imsave('test.jpg', imgar)
    return render_template("next.html",image="static/cloud.jpg")
    # return redirect(url_for('static',filename='cloud.jpg'))

def __get_oauth_ver():
    return request.args.get("oauth_verifier", "Not defined")

def __get_username(api):
    return (api.me()._json)['screen_name']

def __get_stopwords():
    stop_words = ['てる','いる','なる','れる','する','ある','こと','これ','さん','して','くれる','やる','くださる','そう','せる','した','思う','それ','ここ','ちゃん','くん', '', 'て','に','を','は','の','が','と','た','し','で','ない','も','な','い','か','ので','よう',' ','https','CO','RT','*','笑','さん','すぎ','いい']
    return stop_words

def __get_API():
    auth.get_access_token(__get_oauth_ver())
    auth.set_access_token(auth.access_token,auth.access_token_secret)
    return tweepy.API(auth)

def create_wordcloud(text):
    fpath = "/Library/Fonts/AppleSDGothicNeo-ExtraBold.otf"
    word = WordCloud(background_color="black",font_path=fpath,width=1000,height=1500).generate(text)
    return word

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80,threaded=True)
