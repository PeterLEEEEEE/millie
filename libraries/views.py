import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from users.models import User
from books.models import Book, Comment


