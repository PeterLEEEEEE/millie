import bcrypt, jwt
import json
import unittest

from django.test import Client, TestCase
from django.conf import settings

from unittest.mock import MagicMock, patch
from .models import *
from my_settings import ALGORITHM


class BookDetailViewTest(TestCase):
    def setUp(self):
        Publisher.objects.create(
                id = 1,
                name         = '김영사',
                introduction = 
                            '''우리는 독자를 섬깁니다.'''
        )
        
        BookInfo.objects.create(
                id = 1,
                text = '본문1',
                contents = '목차1'
        )
        
        Book.objects.create(
            id              = 1,
            title           = '열두시에 라면을 끓인다는 건',
            publish_date    = '2019-02-05',
            description     = '''딱히 배가 고픈 건 아닌데''',
            page            = 320,
            image_url       = 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
            publisher_id    = 1,
            book_info_id    = 1
        )

        Category.objects.create(
                id = 1,
                name = '에세이'
            )

        BookCategory.objects.create(
            book_id = 1,
            category_id = 1,
        )

        Author.objects.create(
                id   = 1,
                name = '정다이',
                introduction = '''"인생은 사랑이 다야."라고 말하는 로맨티스트.'''
            )

        BookAuthor.objects.create(
            id = 1,
            book_id = 1,
            author_id = 1,
        )

    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()

    def test_bookdetailview_get_success(self):
        client = Client()
        response = client.get('/books/1',content_type='application/json')
        
        self.assertEqual(response.json(),
            {
                "RESULT": {
                    "title"          : '열두시에 라면을 끓인다는 건',
                    "image_url"      : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                    "book_intro"     : '''딱히 배가 고픈 건 아닌데''',
                    "publisher"      : '김영사',
                    "publisher_intro": '''우리는 독자를 섬깁니다.''',
                    "book_contents"  : '목차1',
                    "pages"          : 320,
                    "publish_date"   : '2019.02.05',
                    "authors"        : ['정다이'],
                    "authors_intro"  : ['"인생은 사랑이 다야."라고 말하는 로맨티스트.'],
                    "category"       : '에세이'
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_bookdetailview_get_doesnotexist(self):
        client = Client()

        response = client.get('/books/2', content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "BOOK DOES NOT EXIST"
            }
        )
        