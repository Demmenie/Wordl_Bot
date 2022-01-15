#11/01/2022
#Chico Demmenie
#Wordl_Bot/main.py

import tweepy
import csv
import json
import time
from datetime import datetime

class main:

    """Main class and loop of the bot"""

    #---------------------------------------------------------------------------
    def __init__(self):

        """Initialising the functions of the loop and getting auth."""

        #Retrieving OAuth Twitter keys.
        self.keys = json.load(open("keys.json", "r"))
        self.DoneReplies = []

        #Requesting an auth from twitter so we can use their API.
        self.api = tweepy.Client(bearer_token=self.keys["bearerToken"],
            consumer_key=self.keys["apiKey"],
            consumer_secret=self.keys["apiSecret"],
            access_token=self.keys["accessToken"],
            access_token_secret=self.keys["accessSecret"],
            wait_on_rate_limit=True)

        self.thisTweetTime = time.time() - 3600
        self.replyList = self.getReplies()

        self.analyseReplies()
        self.postReplies()


    #---------------------------------------------------------------------------
    def makeWordl(self):

        """A function that gets the next wordl and posts it."""

        wordls = open("wordls.csv", "r")
        wordls = csv.reader(wordls, delimiter=',')

        self.thisWordl = wordls[self.day]
        tweet = ''.join(("Wordl ", self.day, "\N{black large square}"+
            "\N{black large square}\N{black large square}\N{black large square}"
            +"\N{black large square}"))

        self.api.create_tweet(text=tweet)
        self.thisTweetTime = int(time.time())


    #---------------------------------------------------------------------------
    def getReplies(self):

        """A function that gets all the unread replies to the latest wordl."""

        latestTweets = self.api.get_users_tweets(id = self.keys["userID"],
            max_results = 5)[0]
        self.thisTweetID = latestTweets[0].id

        replies = self.api.search_recent_tweets(query="to:BotWordl",
            max_results=100,
            start_time=datetime.fromtimestamp(self.thisTweetTime))

        return replies.data


    #---------------------------------------------------------------------------
    def analyseReplies(self):

        """A function that looks at the replies and finds out if they're
        correct."""

        for reply in self.replyList:

            replySplit = reply.text.split(" ")
            if replySplit[0] == "@BotWordl" and (len(replySplit == 2) or
                len(replySplit == 3):

                if len(replySplit[-1]) != 5:
                    message = "Sorry, that word is the wrong length."
                    self.TweetReply(reply.id, message)

                elif replySplit[-1] == self.thisWordl[0]:
                    message = ''.join("\N{green square}\N{green square}"+
                        "\N{green square}\N{green square}\N{green square} "+
                        f"\n{self.thisWordl[0]} - {self.thisWordl[2]}"

                    self.TweetReply(reply.id, message)

                else:
                    thisGuess = list(replySplit[-1])



    #---------------------------------------------------------------------------
    def TweetReply(self, replyID, message):

        """A function that replies to tweets"""

        self.api.create_tweet(text=message, in_reply_to_tweet_id=replyID)

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
