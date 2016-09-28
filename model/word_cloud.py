#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tweepy
import MeCab
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy as sp
sys.path.append("/Library/Python/2.7/site-packages")

class wc:
    def __init__(self):
        self.mt = MeCab.Tagger("mecabrc")

    def make_picture(self,api):
        textl = []
        stop_words = self.__get_stopwords()
        for tweet in tweepy.Cursor(api.user_timeline, id=self.__get_username(api)).items(70):
            res = self.mt.parseToNode(str(tweet.text.encode("utf-8")))
            while res:
                feat = res.feature.split(",")
                if (feat[0] == "名詞" or feat[0] == "形容詞" or feat[0] == "副詞") and (res.surface.isalpha() == False) and (res.surface.isdigit() == False) and (res.surface not in stop_words):
                    textl.append(feat[6])
                res = res.next

        wc_pic = self.__create_wordcloud(" ".join(textl).decode("utf-8"))
        plt.figure(figsize=(13,16))
        plt.imshow(wc_pic)
        plt.axis("off")
        plt.savefig("/Users/chan-p/GitHub/Twitter-Analysis/static/cloud.jpg", bbox_inches='tight', pad_inches=0.0)

    def __get_stopwords(self):
        stop_words = ['てる','いる','なる','れる','する','ある','こと','これ','さん','して','くれる','やる','くださる','そう','せる','した','思う','それ','ここ','ちゃん','くん', '', 'て','に','を','は','の','が','と','た','し','で','ない','も','な','い','か','ので','よう',' ','https','CO','RT','*','笑','さん','すぎ','いい']
        return stop_words

    def __create_wordcloud(self,text):
        fpath = "/Library/Fonts/Klee.ttc"
        word = WordCloud(background_color="black",font_path=fpath,width=1000,height=1500).generate(text)
        return word

    def __get_username(self,api):
        return (api.me()._json)['screen_name']
