from django.urls import path
from libraries.views import (
    ShelfDeleteView, 
    LibraryListView, 
    LibraryView,
    ShelfListView, 
    ViewerView,
    ShelfView,
)

urlpatterns = [
    path('', LibraryView.as_view()),
    path('/shelfdelete', ShelfDeleteView.as_view()),
    path('/shelf', ShelfView.as_view()),
    path('/<int:book_id>', LibraryListView.as_view()),
    path('/shelflist', ShelfListView.as_view()),
    path('/<int:book_id>/viewer', ViewerView.as_view()),
]