from twitterHandler import Twitter_User



if __name__=='__main__':
    user = Twitter_User.Twitter_User(id)
    user.get_tweets()
    best_tweets = user.most_liked_rt()
    hashtags = user.count_hashtags(best_tweets)
    print(best_tweets)
    print(hashtags)












