from twitterStreaming import TwitterStreaming
import time

if __name__ == '__main__':
    twitterStreaming = TwitterStreaming()
    print("start streaming")
    twitterStreaming.start(['taiwan'])
