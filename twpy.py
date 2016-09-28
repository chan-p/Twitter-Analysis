#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import tweepy

# 各種キーをセット
CONSUMER_KEY = 'SjT3DTgX44ZCfLpk8cs7Joncb'
CONSUMER_SECRET = 'IeIk6PYvhkDLIJd7cQp8ZV6mLSQuLS76jQOphCFo2TWPF6K60d'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# 以下は、アクセストークンをもらいにいく場合のコード。
# まず、認証コードを貰いに行くアドレスを取得する
redirect_url = auth.get_authorization_url()

# アドレスを表示し、ブラウザでアクセスして認証用コードを取得してくる。
# べつにGetなんたらはなくてもよく、redirect_urlをprintするだけでもよい。
print 'Get your verification code from: ' + redirect_url

# ブラウザから取得してきた認証用コードを対話モードで入力する。
# strip()はコピペの際に末尾に改行コードとかスペースが入ったのを消すため。
verifier = raw_input('Type the verification code: ').strip()


# Access TokenとAccess Token Secretを取得してそれぞれオブジェクト
# として格納しておく。
auth.get_access_token(verifier)
ACCESS_TOKEN = auth.access_token
ACCESS_SECRET = auth.access_token_secret

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#APIインスタンスを作成
api = tweepy.API(auth)

# これだけで、Twitter APIをPythonから操作するための準備は完了。
print('Done!')
