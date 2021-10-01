from django.urls import path
from books.views import (
    CommentLikeView, 
    CommentView, 
    BookGenreView, 
    BookDetailView,
    MovieRecommend,
    SearchMainView,
    SearchView,
    BookPublisherView,
    NewBooksView
)

urlpatterns = [
    path('/<int:book_id>/comments', CommentView.as_view()),
    path('/comments-like', CommentLikeView.as_view()),
    path('/genre', BookGenreView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/search', SearchView.as_view()),
    path('/search/Main', SearchMainView.as_view()),
    path('/recommend', MovieRecommend.as_view()),
    path('/publisher',BookPublisherView.as_view()),
    path('/new',NewBooksView.as_view()),
]
