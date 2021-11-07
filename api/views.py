from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.twitterUtil import (get_media_urls_using_tweet_id, tweet_with_media,
                             tweet_without_media)


# Create your views here.
class QuoteTweet(APIView):
    """
    End point to make a Quote Tweet. This end point expecects following data in payload
    >>> payload = {
        'text':str, string in the quote tweet,
        'quote_tid':int, id of the tweet that is quoted
        'media_tid':INT | None, OPTIONAL,  id of tweet from where media is to be taken, 
                   send none if not applicable.
    }
    >>> # send it like this
    >>> requests.post('/quote-tweet/, data = payload, auth=(username, password))
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data     
        # <QueryDict: {'text': ['this is text'], 'id': ['1'], 'has_media': ['False']}>
        text = request.data.get('text', '')
        quote_tid = request.data.get('quote_tid', None)
        media_tid = request.data.get('media_tid', None)

        if quote_tid is None:
            return Response({
                'detail':"Tweet Id (id) is not given",
            }, 400)
        
        # if 'media_tid' is given then fetch url of all media present in tweet with id 'media_tid'
        media_urls = (get_media_urls_using_tweet_id(media_tid) if media_tid else [])


        # if there is any media, then tweet with media otherwise not
        try:
            if media_urls:
                tweet_with_media(media_urls, text, quote_tid)
            else:
                tweet_without_media(text, quote_tid)
        except Exception as e:
            text = f"Something went wrong. ERROR from tweeter api ->  {e}"
            return Response({'detail':text}, 500)

        return Response({'text':text, 'quote_tid':quote_tid,'media_tid':media_tid})