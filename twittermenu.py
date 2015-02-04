def followkeyword():
		amount = 0
		keyword = raw_input("keyword to follow: ")
		amount = raw_input("amount to follow: ")
		auto_follow(keyword, amount)

def retweetkeyword(keyword, amount):
		amount = 0
		keyword = raw_input("keyword to retweet: ")
		amount = raw_input("amount to retweet: ")
		auto_rt(keyword, amount)

def favkeyword(keyword, amount):
		amount = 0
		keyword = raw_input("keyword to favourite: ")
		amount = raw_input("amount to favourite: ")
		auto_fav(keyword, amount)


def unfollowall():
		confirm = raw_input("yes or no?: ")
		if confirm == "yes":
			auto_unfollow_nonfollowers()
		elif confirm == "no":
			print "cool cool, everyone still exists :D"

def followback():
		auto_follow_followers()

from ubertwitdef import *
#6footGeek.com twitter bot
choice = True
while choice:
	print "welcome to the 6footGeek twitterbot v1"
	print """1 - follow a particular keyword"
			2 - Automatically retweet any tweets with a keyword
			3 - Automatically favorite any tweets with a keyword
			4 - Automatically unfollow all users that dont follow me
			5 - Auto follow everyone who follows you
			0 - exit"""
	choice = raw_input("Enter a menu choice!")
	if choice == "1":
		followkeyword()
	elif choice == "2":
	    retweetkeyword()
	elif choice == "3":
		favkeyword()
	elif choice == "4":
	    unfollowall()
	elif choice == "5":
	    followback()
	elif choice == "0":
		choice == False
		break
	else:
	    print "invalid operator"
	    break
