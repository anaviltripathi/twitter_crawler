from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "880470613-m37gutx48zeE4byeH5Qf37E4YlaRXOwS6gd4CN24"
access_token_secret = "TRdP9Lp0PiRO42a73f7MCkmThqYwCTRaFhdZaCWTPasLQ"
consumer_key = "1mfASla0gTaa3SF1Wm9IhRB6p"
consumer_secret = "TM0CKlkeWPRzCMG3alxDDWtnGmsFNnvoOYiqZf1ZJjjqcVLyW1"

#auth.set_access_token(access)

class StdOutListener(StreamListener):
    def on_data(self, raw_data):
        print(raw_data)
        return True
    def on_error(self, status):
        print(status)



if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
