from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
import gettweets as gt
import json

def sentiment(content):

    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    return(sentiment.score, sentiment.magnitude)
if __name__ == '__main__':
    tweets = []
    with open('tweettext.json') as file:
        tweets = json.load(file)
    score=0
    mag=0
    count = 0
    for i in range(len(tweets)) :
        score += sentiment(tweets[i][0])[0]
        mag += sentiment(tweets[i][0])[1]
        count += 1
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
