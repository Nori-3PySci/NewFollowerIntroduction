# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import tweepy
import datetime
import random
import csv

account = "@account"

n_people = 1

time_now = datetime.datetime.now()

previous_file = r"/absolute path/previous_follower_list.csv"

consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
access_token = 'access token'
access_token_secret = 'access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)


# -

def previous_follower_listing(previous_file):
    
    previous_list = []
    
    with open(previous_file, "r") as file:
        reader = csv.reader(file)
        
        for row in reader:
            previous_list.append(int(row[0]))
            
    return previous_list


def follower_listing(account):
    
    follower_id_all = tweepy.Cursor(api.followers_ids, id = account, cursor = -1).items()
    
    f_list = []
    
    for follower_id in follower_id_all:
        f_list.append(follower_id)
    
    return f_list


def get_name(id_list):
    
    n_list = []
    
    for user_id in id_list:
        n_list.append("@" + api.get_user(user_id).screen_name)
        
    return n_list


def intro_tweet(intro_name_list, n_people, time_now):
    if len(intro_name_list) != 0:
        tweet_content = '\n\n'.join(intro_name_list)
        api.update_status("新しいフォロワーさんのなかからランダムで" + str(n_people) +"人紹介！\n\n" +  tweet_content + "\n\nフォローありがとうございました！\n\n" + time_now.strftime("%Y/%m/%d %H:%M:%S") + "\n\n#新規フォロー感謝砲") 


def main(account, time_now, n_people, previous_file):
    current_follower = follower_listing(account)
    prev_follower = previous_follower_listing(previous_file)
    
    new_follower = []
    
    for cf in current_follower:
        if not cf in prev_follower:
            new_follower.append(cf)
    
    print(len(current_follower), len(prev_follower), len(new_follower))
    
    if len(new_follower) <= n_people:
        intro_id_list = new_follower
    elif len(new_follower) > n_people:
        intro_id_list = random.sample(new_follower, n_people)
        
    intro_name_list = get_name(intro_id_list)
    intro_tweet(intro_name_list, n_people, time_now)
    
    with open(previous_file, "a") as file:
        writer = csv.writer(file)
        for nf in new_follower:      
            writer.writerow([nf])


if __name__ == '__main__':
    main(account, time_now, n_people, previous_file)




