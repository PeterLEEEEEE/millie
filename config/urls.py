from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('books', include('books.urls')),
    path('libraries', include('libraries.urls')),
]
