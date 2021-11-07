## Tweesper
This is an api micro-service to handle twitter handle. I am at the moment using it to automate twitter handle.
This is one part of bigger project I am working on at present on my free time.


## Operational EndPoints
At the moment only these endpoint are operational. I am planning to keep documentation upto date as I move on.

- /api/quote-tweet

    this endpoint uses basic authentication with username and password. It takes following data to work
    
    ```json
    {
        "text": [str] "some text to quote tweet",
        "quote_tid": [int] // id of the tweet to quote,
        "media_tid": [int] // id of the tweet from where media is to be used
    }
    ```

    If backend is successful is creating tweet then it returns 200 resp otherwise appropriate status code and message.

## Todo EndPoints
These endpoints are either underdevelopment or will be added.

- /api/create-tweet

    This endpoint is suppose to create a new tweets. (I have still not decided specifics of this point yet.)

## Environment Setup
Env vars should have following
- twitter_api_key
- twitter_api_key_secret
- twitter_access_token
- twitter_access_token_secret
- twitter_bearer_token
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS (eg 'domain.com')