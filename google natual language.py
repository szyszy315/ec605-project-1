from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
import gettweets as gt
import json
import time
import nltk
from nltk.corpus import stopwords

#get words that most mentioned
def most_frequent(List):
    unimportantwords =stopwords.words('english')
    unimportantwords.extend(["It's","If",'today','I',''])
    count = {}
    for i in List:
        if i in unimportantwords:
            continue
        if i not in count.keys():
            count[i] = 1
        else :
            count[i] += 1
    word = sorted(count.items(),key = lambda x:x[1] ,reverse = True)
    return word[1:4]
#analyze sentiment
def sentiment(content):

    client = language_v1.LanguageServiceClient()

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    return(sentiment.score, sentiment.magnitude)

def split(string):
    st = []
    sp = []
    for i in string:
        sp =i.split(' ')
    for t in sp:
        if (len(t)) > 10:
            continue
        else:
            st.append(t)
    return(st)

if __name__ == '__main__':
#get tweets
    tweets = []
    with open('tweettext.json') as file:
        tweets = json.load(file)
    score=0
    mag=0
    count = 0
    freq = []
    positive = []
    negative = []
#get score and magnitude of google natural language
    for i in range(len(tweets)) :
        score += sentiment(tweets[i][0])[0]
        mag += sentiment(tweets[i][0])[1]
#collect tweets with positive attitude and negative attitude
        if sentiment(tweets[i][0])[0] > 0.2:
            positive.append(tweets[i][0])
        if sentiment(tweets[i][0])[0] < -0.2:
            negative.append(tweets[i][0])
        count += 1
        tww = tweets[i][0].split(' ')
        for t in tww:
            if (len(t)) > 10:
                continue
            else:
                freq.append(t)
    pos = split(positive)
    neg = split(negative)
    posword = most_frequent(pos)
    negword = most_frequent(neg)
    print ('tweets with positive attitude mentioned ', posword)
    print ('tweets with negative attitude mentioned ', negword)
    fre=[]
    fre.append(most_frequent(freq))
    print('the most mentioned word is ',fre)
    score = score / count
    mag = mag / count
    if score > 0.5:
        print('Clearly Positive')
    elif score >= 0.2:
        print('Positive')
    elif score < 0.2 and score > -0.2 and mag <2:
        print ('neutral')
    elif score < 0.2 and score > -0.2 and mag > 2:
        print('mixed')
    elif score <= - 0.2 and score > -0.5:
        print(' Negative')
    else: print('Clearly Negative')
    input('input anything to continue...')

