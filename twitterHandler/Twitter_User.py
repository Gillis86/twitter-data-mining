import tweepy
import pandas as pd
import twitterHandler.twitter_data
import collections


auth = tweepy.OAuthHandler(twitterHandler.twitter_data.consumer_key, twitterHandler.twitter_data.consumer_secret)
auth.set_access_token(twitterHandler.twitter_data.access_token, twitterHandler.twitter_data.access_secret)
api = tweepy.API(auth)


class Twitter_User():
    '''Get information about a specific Twitter User'''
    def __init__(self, id, count=200):
        self.id = id
        self.count = count
        self.data = None
        self.like_average = None
        self.rt_average = None

    def get_tweets(self): #store last n tweets in a dataframe
        simple_list = []
        try:
            for status in tweepy.Cursor(api.user_timeline, id=self.id).items(self.count):
                array = [status._json["text"].strip(), status._json["favorite_count"],
                         status._json["created_at"], status._json["retweet_count"],
                         [h["text"] for h in status._json["entities"]["hashtags"]],status._json["lang"]]
                simple_list.append(array)
            self.data = pd.DataFrame(simple_list, columns=["Text", "Like", "Created at", "Retweet", "Hashtags","Lang"])
            self.data = self.data[~self.data["Text"].str.startswith('RT')]
            return self.data
        except tweepy.TweepError:
            return tweepy.TweepError.message[0]['code']
        except tweepy.RateLimitError:
            rate = api.rate_limit_status()
            return rate

    def __repr__(self): #give a repr of the user
        user = api.get_user(self.id)
        return "User name: {0}\n" \
               "User screen name: {1}\n" \
               "Location: {2}\n" \
               "User description: {3}\n"\
                "Url: {4}\n" \
               "Followers {5}".format(user._json['name'],user._json['screen_name'],user._json['location'],
                                      user._json['description'],user._json['url'],user._json['followers_count'])

    def most_liked_rt(self): #return a df of tweets where the number of like and rt is greater than respective averages
        self.like_average = self.data["Like"].mean()
        self.rt_average = self.data["Retweet"].mean()
        return self.data.loc[(self.data['Like'] > self.like_average) & (self.data['Retweet'] > self.rt_average)]

    def count_hashtags(self,df): #give the most used hashtags in the tweets df - to use with the return df of most_liked_rt()
        h_tags_cloud = []
        h_tags = df[['Hashtags', 'Created at']]
        h_tags = h_tags[h_tags["Hashtags"].map(len) != 0]
        h_tags_list = h_tags["Hashtags"].tolist()
        h_tags_counter = collections.Counter()
        for h_inner_list in  h_tags_list:
            for h_element in h_inner_list:
                h_tags_cloud.append(h_element)
        h_tags_counter.update(h_tags_cloud)
        h_tags_df = pd.DataFrame.from_dict(h_tags_counter,orient="index").sort_values(0,ascending=False)
        h_tags_df = h_tags_df.rename(columns={0: 'HashTags Freq'})
        return h_tags_df






