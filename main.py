#11/01/2022
#Chico Demmenie
#Wordl_Bot/main.py

#Getting dependencies
import tweepy
import csv
import json
import time
import re
from datetime import datetime


class main:

    """Main class and loop of the bot"""


    #---------------------------------------------------------------------------
    def __init__(self):

        """Initialising the functions of the loop and getting auth."""

        print("Initialising...")
        #Retrieving OAuth Twitter keys.
        self.keys = json.load(open("keys.json", "r"))

        #Setting variables we need beforehand.
        self.doneReplies = []
        self.peopleWhoGuessed = []
        self.day = self.keys["thisDay"]
        self.authTime = None
        self.thisTweetTime = time.time() - 80000

        self.mainLoop()


    #---------------------------------------------------------------------------
    def mainLoop(self):

        """The main loop of the bot that calls functions."""

        print("Entering main loop...")
        while True:
            self.wordlAnswer = False
            self.makeWordl

            #if (time.time() - 86400) > self.thisTweetTime:
            self.makeWordl()
            while self.wordlAnswer == False:
                #Checking if we need a new authentication and requesting.
                if (self.authTime == None or
                    (self.authTime + 7100) < time.time()):

                    self.api = tweepy.Client(
                        bearer_token=self.keys["bearerToken"],
                        consumer_key=self.keys["apiKey"],
                        consumer_secret=self.keys["apiSecret"],
                        access_token=self.keys["accessToken"],
                        access_token_secret=self.keys["accessSecret"],
                        wait_on_rate_limit=True
                        )

                #Calling the necessary functions
                self.replyList = self.getReplies()
                self.analyseReplies()

                #if (time.time() - 86400) > self.thisTweetTime:
                    #self.reset()
                    #break

                time.sleep(6)


    #---------------------------------------------------------------------------
    def makeWordl(self):

        """A function that gets the next wordl and posts it."""

        #Grabbing the csv of wordls
        print("Making Wordl...")
        file = open("wordls.csv", "r")
        wordls = csv.reader(file)

        #Finding today's Wordl
        for index, line in enumerate(wordls):
            if index == self.day:

                self.thisWordl = line
                break

        #Creating the day's tweet
        tweet = ''.join(("Wordl ", str(self.day),
            "\n\U00002B1B\U00002B1B\U00002B1B\U00002B1B\U00002B1B"))

        #self.api.create_tweet(text=tweet)
        #self.thisTweetTime = int(time.time())

        print(f"Wordl {self.day}: {self.thisWordl[0]} - time: {time.time()}")


    #---------------------------------------------------------------------------
    def getReplies(self):

        """A function that gets all the unread replies to the latest wordl."""

        try:
            print("Getting replies...")
            replies = self.api.search_recent_tweets(query="to:BotWordl",
                max_results=100,
                #start_time=datetime.fromtimestamp(self.thisTweetTime),
                expansions='author_id')

        except Exception as e:
            print(e)


        print("Replies:", replies.data)
        return replies.data


    #---------------------------------------------------------------------------
    def analyseReplies(self):

        """A function that looks at the replies and finds out if they're
        correct."""

        for reply in self.replyList:

            #Creating variables needed during the logic
            message = []
            replySplit = reply.text.split(" ")

            #Making sure that the message was in reply to the bot
            if (replySplit[0] == "@BotWordl" and
                (len(replySplit) == 2 or len(replySplit) == 3)):

                if reply.id not in self.doneReplies:
                    self.doneReplies.append(reply.id)
                    
                    if reply.author_id not in self.peopleWhoGuessed:

                        #Making sure that the word is the right length
                        if len(replySplit[-1]) != 5:
                            message = "Sorry, that word is the wrong length."
                            self.TweetReply(reply.id, message)

                        #Finding out if the user answered the wordl correctly
                        elif replySplit[-1] == self.thisWordl[0]:
                            message = ''.join(("\U0001F7E9\U0001F7E9\U0001F7E9"+
                                "\U0001F7E9\U0001F7E9"+
                                f"\n{self.thisWordl[0]} - {self.thisWordl[2]}"))

                            self.TweetReply(reply.id, message)
                            self.retweetReply(reply.id)
                            self.wordlAnswer = True
                            self.reset()
                            break

                        #If none of the above are true then we work out what the user
                        #got rght and wrong.
                        else:
                            self.peopleWhoGuessed.append(reply.author_id)
                            thisGuess = list(replySplit[-1])
                            wordlList = list(self.thisWordl[0].upper())

                            #A for loop that checks each letter of the answer.
                            for index, letter in enumerate(thisGuess):

                                if letter.upper() == wordlList[index]:
                                    message.append(("\U0001F7E9"))

                                elif letter.upper() in wordlList:
                                    message.append(("\U0001F7E8"))

                                else:
                                    message.append(("\U00002B1B"))

                    else:
                        message = "You may only have one guess per Wordl."

                    message = ''.join(message)
                    self.TweetReply(reply.id, message)


    #---------------------------------------------------------------------------
    def TweetReply(self, replyID, message):

        """A function that replies to tweets."""
        print("Replying:", message, "to:", replyID)

        try:
            self.api.create_tweet(text=message, in_reply_to_tweet_id=replyID)

        except Exception as e:
            print(f"error: {e}")


    #---------------------------------------------------------------------------
    def RetweetReply(self, replyID):

        """A function that retweets any tweet based on a given id."""

        try:
            self.api.retweet(tweet_id=replyID)

        except Exception as e:
            print(e)


    #---------------------------------------------------------------------------
    def reset(self):

        """Resets variables and gets ready for the next wordl."""

        self.day = self.day + 1
        self.keys["thisDay"] = self.day
        open("keys.json", "w").write(json.dumps(self.keys))
        self.peopleWhoGuessed = []
        self.doneReplies = []
        self.replyList


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
