from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API
import json, sys
from random import random
from collections import defaultdict
with open("config.txt", 'r') as f:
    consumer_key = f.readline().strip()
    consumer_secret = f.readline().strip()
    access_token = f.readline().strip()
    access_token_secret = f.readline().strip()

# class Search:
#     def __init__(self):    
#        auth = OAuthHandler(consumer_key, consumer_secret)
#        auth.set_access_token(access_token,access_token_secret)
#        self.api= API(auth)

#    def getUser(self, user_id):
#        return self.api.lookup_users(user_ids=[user_id])

#    def getUserByName(self, username):
#        return self.api.get_user(username)
# def jdefault(ob):
#     return ob.__dict__

class StdOutListener(StreamListener):
    i = 0
    # s = Search()
    def on_data(self, data):
        json_tweet = json.loads(data)
        if "created_at" in json_tweet:
            if self.i >= 1:
                sys.exit()
            
            tweet = json_tweet["text"]
            user_id = json_tweet['user']['id']
            reconstructed_tweet = defaultdict(dict)
            if len(tweet) > 120:
                self.i += 1

                #for key in json_tweet:
                list_of_tweet_attribs = ['id', 'text', 'source', 'coordinates', 'timestamp_ms', 'geo', 'entities', 
                                            'retweet_count', 'favorited', 'favorite_count', 'retweeted', 'created_at']
                for attr in list_of_tweet_attribs:
                    if attr in json_tweet:
                        reconstructed_tweet[attr] = json_tweet[attr]
                
                
                list_of_user_attribs = ['id', 'name', 'location', 'created_at', 'screen_name', 'statuses_count', 
                                        'friends_count', 'followers_count', 'time_zone', 'retweeted_status', 'description',
                                        'url', 'geo']

                for attr in list_of_user_attribs:
                    if attr in json_tweet['user']:
                        reconstructed_tweet['user'][attr] = json_tweet['user'][attr]
                
                if 'retweeted_status' in json_tweet:
                    rt_status = reconstructed_tweet['retweeted_status']
                    rt_status['user'] = {}
                    rt_tweet_original = json_tweet['retweeted_status']
                    list_of_tweet_attribs = ['id', 'text', 'source', 'coordinates', 'timestamp_ms', 'geo', 'entities', 
                                            'retweet_count', 'favorited', 'favorite_count', 'retweeted', 'created_at']
                    
                    for attr in list_of_tweet_attribs:
                        if attr in rt_tweet_original:
                            rt_status[attr] = rt_tweet_original[attr]
                    
                    #if 'user' in rt_tweet_original:
                    list_of_user_attribs = ['id', 'name', 'location', 'created_at', 'screen_name', 'statuses_count', 
                                          'friends_count', 'followers_count', 'time_zone', 'retweeted_status', 'description',
                                           'url', 'geo']
                    for attr in list_of_user_attribs:
                        if attr in rt_tweet_original['user']:
                            rt_status['user'][attr] = rt_tweet_original['user'][attr]
        


                print("Final pretty tweet: \n")
                print(json.dumps(reconstructed_tweet, indent=4))

                print("found new tweet now creating file")
                with open(".././data/tweet_{0}".format(self.i), 'w') as f:
                    
                    u_removed_tweet = json.dumps(json_tweet)
                    f.write(str(u_removed_tweet))
                    
                # if random() > 0:
                #     print("creating new user")
                #     with open(".././user_data/user {0}".format(self.i), 'w') as usr:
                #         usr_profile = self.s.getUser(user_id)
                #         #print(str(self.s.getUser(user_id)))
                #         print(type(usr_profile))
                #         print(usr_profile)
                #         print(dir(usr_profile))
                #         user_json = json.dumps(usr_profile, default=jdefault)
                #         print(user_json)
                #         usr.write(str(user_json))

        return True



    
    # def on_status(self, status):
    #     if self.i >= 1:
    #         sys.exit(0)
    #     tweet = status.text
    #     #coordinates = str(status.coordinates) if status.coordinates else ""
    #     user = status.author.screen_name
    #     userid = str(status.author.id)
    #     #time = str(status.created_at)
    #     #source = status.source
    #     #tweetid = str(status.id)
    #     type(status)
    #     #status.keys()
    #     if len(tweet) >= 100:
    #         self.i += 1
    #         print("found new tweet now creating file")
    #         with open(".././data/tweet {0}".format(self.i), 'w') as f:
    #             print(str(status))
    #             print(str(status)[7:-1])
    #             print(json.loads(str(status)[7:-1]))
    #             f.write(json.loads(status))
    #             f.write("tweet: {0} \n".format(tweet))
    #             f.write("coordinates: {0} \n".format(coordinates))
    #             f.write("user: {0} \n".format(user))
    #             f.write("userid: {0} \n".format(userid))
    #             f.write("time: {0} \n".format(time))
    #             f.write("source: {0} \n".format(source))
    #             f.write("tweetid: {0} \n".format(tweetid))
    #     return True

    def on_error(self, status):
        print(status)

    def on_delete(self, status_id, user_id):
        print("Delete notice for {0}, {1}".format(status_id, user_id))
        return
    
    def on_limit(self, track):
        # Called when a limitation notice arrvies
        print("!!! Limitation notice received: %s" % str(track))
        return


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(languages=['en'], track=['the', 'be', 'to', 'of', 'and', 'a', 
                                            'in', 'that', 'have', 'I', 'it', 'for', 
                                            'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'])
    #stream.sample()