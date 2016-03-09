from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


with open("config.txt", 'r') as f:
    consumer_key = f.readline().strip()
    consumer_secret = f.readline().strip()
    access_token = f.readline().strip()
    access_token_secret = f.readline().strip()

import sys
class Search(object):
    def __init__(self):    
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        self.api=tweepy.API(auth)

    def getUser(self, user_id):
        return self.api.lookup_users(user_ids=[user_id])

    def getUserByName(self, username):
        return self.api.get_user(username)
        
class StdOutListener(StreamListener):
    i = 0
    def on_status(self, status):
        if self.i >= 100000:
            sys.exit(0)
        tweet = status.text
        coordinates = str(status.coordinates) if status.coordinates else ""
        user = status.author.screen_name
        userid = str(status.author.id)
        time = str(status.created_at)
        source = status.source
        tweetid = str(status.id)
        if len(tweet) >= 100:
            self.i += 1
            print("found new tweet now creating file")
            with open(".././data/tweet {0}".format(self.i), 'w') as f:
                f.write("tweet: {0} \n".format(tweet))
                f.write("coordinates: {0} \n".format(coordinates))
                f.write("user: {0} \n".format(user))
                f.write("userid: {0} \n".format(userid))
                f.write("time: {0} \n".format(time))
                f.write("source: {0} \n".format(source))
                f.write("tweetid: {0} \n".format(tweetid))
        return True

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