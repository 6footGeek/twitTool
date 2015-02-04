from twitter import Twitter, OAuth, TwitterHTTPError
import os
from secrets import *


ALREADY_FOLLOWED_FILE = "already-followed.csv"
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))
amount = 0

def search_tweets(q, count=amount, result_type="recent"):
    return t.search.tweets(q=q, result_type=result_type, count=amount)


def auto_fav(q, count=amount, result_type="recent"):
    result = search_tweets(q, count, result_type)
    for tweet in result["statuses"]:
        try:
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue
            result = t.favorites.create(_id=tweet["id"])
            ticker = ticker + 1
            print("favorited: %s" % (result["text"].encode("utf-8")))
            print(ticker)
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def auto_rt(q, count=amount, result_type="recent"):
    result = search_tweets(q, count, result_type)
    for tweet in result["statuses"]:
        try:
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue
            result = t.statuses.retweet(id=tweet["id"])
            print("retweeted: %s" % (result["text"].encode("utf-8")))
        except TwitterHTTPError as e:
            print("already retweeted")


def auto_follow(q, amount, result_type="recent"):
    result = search_tweets(q, amount, result_type)
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")
    do_not_follow = set()
    dnf_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            dnf_list.append(int(line))
    do_not_follow.update(set(dnf_list))
    del dnf_list
    for tweet in result["statuses"]:
        try:
            if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                    tweet["user"]["id"] not in following and
                    tweet["user"]["id"] not in do_not_follow):
                t.friendships.create(user_id=tweet["user"]["id"], follow=True)
                following.update(set([tweet["user"]["id"]]))
                print("followed %s" % (tweet["user"]["screen_name"]))
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))
            if "blocked" not in str(e).lower():
                quit()


def auto_follow_followers():
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
    not_following_back = followers - following
    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=True)
        except Exception as e:
            print("error: %s" % (str(e)))


def auto_unfollow_nonfollowers():
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
    users_keep_following = set([])
    not_following_back = following - followers
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")
    already_followed = set(not_following_back)
    af_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            af_list.append(int(line))
    already_followed.update(set(af_list))
    del af_list
    with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")
    for user_id in not_following_back:
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print("unfollowed %d" % (user_id))
