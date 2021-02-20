import os
import pickle5 as pickle
import boto3

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

aws_s3 = boto3.client(
    's3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_ACCESS_KEY
)


try:
    with open('wordlist.pickle', 'wb') as f:
        aws_s3.download_fileobj('bot-bez-bot-bucket', 'wordlist.pickle', f)

    with open('wordlist.pickle', 'rb') as handle:
        wordlist = pickle.load(handle)
except Exception as e:
        print('Wordlist not found!\n', e)
        wordlist = []


def s3_sync(data):
    with open('wordlist.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    aws_s3.upload_file('wordlist.pickle', 'bot-bez-bot-bucket', 'wordlist.pickle')