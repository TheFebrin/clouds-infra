import urllib.request
import json
import io
from PIL import Image
from google.cloud import storage
from google.appengine.api import images


def get_random_quote() -> str:
    url: str = 'https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=?'
    try:
        req = urllib.request.Request(url, headers = {'User-Agent' : 'Magic Browser' })
        text = urllib.request.urlopen(req).read().decode()
        text = text.strip('?').lstrip('(').rstrip(')')
        random_quote = json.loads(text)['quoteText']
    except Exception as e:
        message = f'Error while downloading the quote: {e}'
        print(message)
        random_quote = message
    return random_quote


def get_increment_and_save_n_button_clicks(increment: bool):
    with open('data/n_button_clicks.txt', 'r+') as f:
        contents = f.readlines()
        if len(contents) == 0:
            n_button_clicks = 0
        else:
            n_button_clicks = int(contents[0])

    if increment:
        with open('data/n_button_clicks.txt', 'w') as f:
            f.write(str(n_button_clicks + 1))
    return n_button_clicks


def get_image_from_bucket():
    """
    The blobstore and images APIs are available only within the App Engine runtime environment
    https://stackoverflow.com/questions/26987062/how-to-serve-google-cloud-storage-images
    """
    # serving_url = images.get_serving_url(
    #     None,
    #     filename='/gs/wiadro-culumbus/flask_server/logo.png'
    # )
    # print(serving_url)
    bucket_url = 'gs://wiadro-culumbus/flask_server/'
    client = storage.Client()

    bucket = client.get_bucket('wiadro-culumbus')

    blob = bucket.get_blob('flask_server/gcs.png')

    raw_image = blob.download_as_string()

    return io.BytesIO(raw_image) 
