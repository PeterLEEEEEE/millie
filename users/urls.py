from django.urls import path

from .views import SocialLoginView

urlpatterns = [
    path('/sign-in/kakao', SocialLoginView.as_view()),
]