import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from stanfordNLP import StanfordNLP



def test_basic():
    with open('tweet_data.json', 'r') as f:
        data = json.load(f)

    #TEST_TEXT = data['text']
    TEST_TEXT = "You are not a pig. do you understand what i mean? I don't like you."
    nlp = StanfordNLP('http://localhost:9000')
    output = nlp.annotate(TEST_TEXT, properties={
        'annotators': 'sentiment',
        'outputFormat': 'json'
    })

    assert len(output['sentences']) > 0
    print('test_basic passed!')

if __name__ == '__main__':
    test_basic()
