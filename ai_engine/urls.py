"""AI Engine URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_api, name='ai_chat'),
    path('recommend/', views.recommend_api, name='ai_recommend'),
    path('fraud-check/', views.fraud_check_api, name='ai_fraud_check'),
    path('sentiment/', views.sentiment_api, name='ai_sentiment'),
    path('predict-price/', views.price_predict_api, name='ai_price_predict'),
    path('fake-review/', views.fake_review_api, name='ai_fake_review'),
]
