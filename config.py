import os
from types import SimpleNamespace
from openai import OpenAI
from firebase_admin import initialize_app, firestore, credentials
# from google.cloud.storage import *
from firebase_admin import storage

if os.environ.get('ON_GOOGLE_CLOUD_RUN') == 'true':
    print('On Google Cloud Run')
    firestore_creds = credentials.ApplicationDefault()
else:
    print('Not on Google Cloud Run')
    from dotenv import load_dotenv
    load_dotenv()
    firestore_creds = credentials.Certificate('firebase_credentials.json')


env = SimpleNamespace(**{
    'on_google_cloud_run': os.environ.get('ON_GOOGLE_CLOUD_RUN'),
    'openai_api_key': os.environ.get('OPENAI_API_KEY'),
})

# Firebase configuration
# https://firebase.google.com/docs/firestore/quickstart
initialize_app(firestore_creds)


clients = SimpleNamespace(**{
    'openai': OpenAI(),
    'firestore': firestore.client(),
    'bucket': storage.bucket(name='stone-fortress-432016-e3.appspot.com')
})


config = SimpleNamespace(**{
    'env': env,
    'clients': clients,
})


if __name__ == "__main__":
    print(config)


