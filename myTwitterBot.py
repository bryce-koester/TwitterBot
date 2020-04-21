import tweepy
import time
print('This is my twitter bot')
#NOTE:
# fill keys with keys obtained from twitter developer account
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



# for mention in mentions:
#     print (str(mention.id)+ ' - ' + mention.text)
#     if '#helloworld' in mention.text.lower():
#         print('Found #HelloWorld')
#         print('responding')

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        text = mention.full_text.lower()
        if '#helloworld' in text:
            print('found #helloworld!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    '#HelloWorld back to you!', mention.id)
        if '#yeet' in text:
            print('found #yeet!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' YEET!', mention.id)
        if '#calculate' in text:
            parse(text, mention)

def parse(text, mention):
    arr = []
    currWord = ''
    function = ''
    args = []
    i = 0
    chr = ''
    while (i < len(text)):
        chr = text[i]
        if (chr == ' '):
            currWord = ''
            i += 1
        if (chr == '('):
            function = currWord
            currWord = ''
            i += 1
            chr = text[i]
            arg = ''
            while ((chr != ')') & (i < len(text))):
                if (chr == ','):
                    args.append(arg)
                    i += 1
                    chr = text[i]
                    arg = ''
                if (chr == ' '):
                    i += 1
                    chr = text[i]
                else:
                    arg += chr 
                    # print(arg)
                    i += 1
                    chr = text[i]
            args.append(arg)
        else:
            currWord += chr
            i += 1
        
    if ((function == '') | (args == [])):
        api.update_status('@' + mention.user.screen_name +
                    ' Invalid function, make sure to follow the format function(arg, arg)', mention.id)   
        print('invalid function')
    else:
        parseExpr(function, args, mention)
def parseExpr(function, args, mention):
    print(args[0])
    print(args[1])
    x = 0
    if (len(args) != 2):
        print('Invalid number of args')
    # multiply
    if ('ultiply' in function):
        x = int(args[0]) * int(args[1])
    # add
    if ('dd' in function):
       x = int(args[0]) + int(args[1])
    # divide
    if ('ivide' in function):
        x = int(args[0]) / int(args[1])
    # subtract
    if ('ubtract' in function):
        x = int(args[0]) - int(args[1])
    if (x == 69):
        api.update_status('@' + mention.user.screen_name +
                    ' Answer: ' + str(x) + ' Nice.', mention.id)
    else:
        api.update_status('@' + mention.user.screen_name +
                    ' Answer: ' + str(x) + ' ', mention.id)
    print('Answer: '+ str(x))
# text = '#calculate subtract(   4 00,   40)'
# null = ''
# parse(text, null)

while True:
    reply_to_tweets()
    time.sleep(15)
