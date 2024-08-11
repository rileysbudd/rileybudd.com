
import os
from types import SimpleNamespace
from openai import OpenAI

if os.environ.get('ON_GOOGLE_CLOUD_RUN') == 'true':
    print('On Google Cloud Run')
else:
    print('Not on Google Cloud Run')
    from dotenv import load_dotenv
    load_dotenv()


env = SimpleNamespace(**{
    'on_google_cloud_run': os.environ.get('ON_GOOGLE_CLOUD_RUN'),
    'openai_api_key': os.environ.get('OPENAI_API_KEY'),
})

clients = SimpleNamespace(**{
    'openai': OpenAI(),
})

config = SimpleNamespace(**{
    'env': env,
    'clients': clients,
})

if __name__ == "__main__":
    print(config)