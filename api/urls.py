from django.urls import path
from api import views

urlpatterns = [
    path('quote-tweet/', views.QuoteTweet.as_view()),
]