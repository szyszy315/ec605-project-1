from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
import gettweets as gt
import json
import time
import nltk
from nltk.corpus import stopwords
#use nltk to filter some commonly used word that i want to ignore
def most_frequent(List):
    unimportantwords =stopwords.words('english')
    unimportantwords.extend(["It's","If"])
    count = {}
    for i in List:
        if i in unimportantwords:
            continue
        if i not in count.keys():
            count[i] = 1
        else :
            count[i] += 1
    word = sorted(count.items(),key = lambda x:x[1] ,reverse = True)
    return word[0:5]

def sentiment(content):

    client = language_v1.LanguageServiceClient()

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    return(sentiment.score, sentiment.magnitude)

if __name__ == '__main__':
#get tweets
    tweets = []
    with open('tweettext.json') as file:
        tweets = json.load(file)
    score=0
    mag=0
    count = 0
    freq = []
#get score and magnitude of google natural language
    for i in range(len(tweets)) :
        score += sentiment(tweets[i][0])[0]
        mag += sentiment(tweets[i][0])[1]
        count += 1
        tww = tweets[i][0].split(' ')
        for t in tww:
            if (len(t)) > 10:
                continue
            else:
                freq.append(t)
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
    elif score <=0.2:
        print(' Negative')
    else: print('Clearly Negative')
    input('input anything to continue...')
