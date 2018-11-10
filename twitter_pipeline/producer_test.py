from producer import TwitterStreaming
import time

if __name__ == '__main__':
    twitterStreaming = TwitterStreaming()
    print("start streaming")

    twitterStreaming.start({'woman'})

    time.sleep(5)
    print('stop streaming')
    twitterStreaming.stop()
    #twitterStreaming.start({'woman'})
    #print("start streaming")
    #time.sleep(5)
