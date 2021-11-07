import tweepy
from tweepy import *
import os

API_KEY = os.environ.get("twitter_api_key", None)
API_KEY_SECRET = os.environ.get("twitter_api_key_secret", None)
ACCESS_TOKEN = os.environ.get("twitter_access_token", None)
ACCESS_TOKEN_SECRET = os.environ.get("twitter_access_token_secret", None)
BEARER_TOKEN = os.environ.get("twitter_bearer_token", None)

if not all([API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    raise Exception(
        f"CANNOT FIND ALL values in env var, {[API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]}"
    )

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True,
)


def upload_media(filepath: str):
    if "https" in filepath or "http" in filepath:
        import urllib.request

        urllib.request.urlretrieve(filepath, "img.jpg")
        media = api.media_upload(
            filename="img.jpg",
        )
    else:
        media = api.media_upload(filepath)
    return media.media_id


def tweet_with_media(filepaths: list, text: str, quote_tweet_id=None):

    if not filepaths:
        tweet_without_media(text, quote_tweet_id)
    else:
        mediaIds = list(map(upload_media, filepaths))
        client.create_tweet(
            quote_tweet_id=quote_tweet_id, media_ids=mediaIds, text=text
        )


def tweet_without_media(text, quote_tweet_id=None):
    client.create_tweet(quote_tweet_id=quote_tweet_id, text=text)


def get_media_urls_using_tweet_id(id):
    """
    id [int|str]
    :returns [list], it returns the list of url of media in tweet
    """
    status = client.get_tweet(
        id,
        expansions="attachments.media_keys",
        media_fields=",".join(
            [
                "alt_text",
                "duration_ms",
                "height",
                "media_key",
                "non_public_metrics",
                "organic_metrics",
                "preview_image_url",
                "promoted_metrics",
                "public_metrics",
                "type",
                "url",
                "width",
            ]
        ),
    )
    media_urls = [media.data["url"] for media in status.includes.get("media", [])]
    return media_urls


if __name__ == "__main__":
    pass
