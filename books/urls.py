"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from books.views import (
    CommentLikeView, 
    CommentView, 
    BookGenreView, 
    BookDetailView,
    MovieRecommend,
    SearchMainView,
    SearchView
)

urlpatterns = [
    path('/<int:book_id>/comments', CommentView.as_view()),
    path('/comments-like', CommentLikeView.as_view()),
    path('/genre', BookGenreView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/search', SearchView.as_view()),
    path('/search/Main', SearchMainView.as_view()),
    path('/recommend', MovieRecommend.as_view()),
    # path('/<int:comment_id>/comment-delete', CommentDeleteView.as_view()),
]
