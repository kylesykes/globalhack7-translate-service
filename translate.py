import json

from multiprocessing.pool import ThreadPool
from functools import partial

# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

def translate(text, target_language, client=translate_client):
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

def endpoint(event, context):
    r = event
    body = json.loads(r['body'])
    text = body['text']
    target_language = body['target_language']

    translated_text = translate(text, target_language)

    response = {
        "statusCode": 200,
        "body": json.dumps(translated_text)
    }

    return response

def translate_array(event, context):
    r = event
    
    body = json.loads(r['body'])
    text_array = body['text']
    target_language = body['target_language']
    
    pool = ThreadPool(10)
    
    partial_translate = partial(translate, target_language=target_language)

    translated_array = pool.map(partial_translate, text_array)

    response = {
        "statusCode": 200,
        "body": json.dumps(translated_array)
    }

    return response

def jaccard_dist(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return float(len(str1 & str2)) / len(str1 | str2)

def double_translate(text, target_language):
    """Translates English text to target language
    then back to English
    """
    translated_text = translate(text, target_language)
    english_text = translate(translated_text, 'en')

    return english_text


def verify(event, context):
    r = event
    body = json.loads(r['body'])
    english_0 = body['text']
    target_language = body['target_language']
    try:
        iterations = body['iterations']
    except KeyError:
        iterations = 3

    english_final = english_0
    for n in range(iterations):
        english_final = double_translate(english_final, target_language)

    #Jaccard, intersection over union
    to_return = {
        "jaccard_dist": jaccard_dist(english_0, english_final),
        "english_0": english_0,
        "english_final": english_final
    }
    
    response = {
        "statusCode": 200,
        "body": json.dumps(to_return)
    }

    return response
