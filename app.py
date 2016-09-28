#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from jinja2 import Environment, FileSystemLoader
from flask import render_template
from flask import request, redirect, url_for
import sys
import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy as sp
sys.path.append("/Library/Python/2.7/site-packages")
sys.path.append("/Users/chan-p/GitHub/Twitter-Analysis/model")
import word_cloud

app = Flask(__name__)
app.config['DEBUG'] = True

# auth = tweepy.OAuthHandler('SjT3DTgX44ZCfLpk8cs7Joncb','IeIk6PYvhkDLIJd7cQp8ZV6mLSQuLS76jQOphCFo2TWPF6K60d')
##Local Version
auth = tweepy.OAuthHandler('wUPAJgKmupzKL5Y97vKeMuCGA','ApxmVcuJLRluNjL3I5cCxQk9hNfNgE5pHYivZnnHzzNDcHT9sb')

@app.route('/')
def Top():
    return render_template("Top.html",url=auth.get_authorization_url())

@app.route('/wordcloud')
def secound():
    word = word_cloud.wc()
    api = __get_API()
    word.make_picture(api)
    return render_template("next.html",image="./static/cloud.jpg",bbox_inches='tight',pad_inches=0.0)

def __get_oauth_ver():
    return request.args.get("oauth_verifier", "Not defined")

def __get_API():
    auth.get_access_token(__get_oauth_ver())
    auth.set_access_token(auth.access_token,auth.access_token_secret)
    return tweepy.API(auth)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80,threaded=True)
