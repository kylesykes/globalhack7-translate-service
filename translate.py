import json

# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

def translate(text, target_language, client=translate_client):
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

def endpoint(event, context):
    r = event
    print(r['body'])
    body = json.loads(r['body'])
    text = body['text']
    target_language = body['target_language']

    translated_text = translate(text, target_language)

    response = {
        "statusCode": 200,
        "body": json.dumps(translated_text)
    }

    return response

