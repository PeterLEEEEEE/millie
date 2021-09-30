import bcrypt, jwt
import json
import unittest

from django.test   import Client, TestCase
from django.conf   import settings

from unittest.mock import MagicMock, patch
from .models       import *
from users.models  import *
from my_settings   import ALGORITHM


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
        response = client.get('/books/1', content_type='application/json')
        
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


class CommentViewTest(TestCase):
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
        
        Platform.objects.create(
            id = 1,
            name = 'Kakao'
        )

        User.objects.create(
            id = 1,
            nickname = 'hyun',
            profile_image_url = 'hyun_url1',
            social_id = '1928131461',
            platform_id = 1,
        )

        Comment.objects.create(
            id = 1,
            book_id = 1,
            user_id = 1,
            text = '야호',
            like_count = 1,
            updated_at = '2021.09.29'
        )

        CommentLike.objects.create(
            id = 1,
            comment_id = 1,
            user_id = 1,
        )
    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
        Platform.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()

    def test_commentview_get_success(self):
        client = Client()
        response = client.get('/books/1/comments', content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                "comments_count": 1,
                "comments": [{
                    "nickname"     : 'hyun',
                    "profile_image": 'hyun_url1',
                    "comment"      : '야호',
                    "comment_id"   : 1,
                    "written"      : '2021.09.30',
                    "likes"        : 1,
                }]
        }, 201)
    
    def test_commentview_get_fail(self):
        client = Client()
        response = client.get('/books/111/comments', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {"MESSAGE": "BOOK DOES NOT EXIST"}
        )

    def test_commentview_post_success(self):
        client = Client()
        
        comment = {
            "text": "11번책 저자 스펙 굳!"
        }
        
        response = client.post('/books/1/comments', json.dumps(comment), **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"}, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {"MESSAGE": "SUCCESS"}
        )

    def test_commentview_post_fail(self):
        client = Client()
        
        comment = {}
        
        response = client.post('/books/1/comments', json.dumps(comment), **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"}, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {"MESSAGE": "WRONG FORMAT"}
        )

    def test_commentview_delete_success(self):
        client = Client()
        response = client.delete('/books/1/comments?comment_id=1', **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"})
        
        self.assertEqual(response.status_code, 204)
    
    def test_commentview_delete_fail(self):
        client = Client()
        response = client.delete('/books/1/comments?comment_id=11', **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"})
        
        self.assertEqual(response.status_code, 401)
    
    def test_commentview_delete_invalid(self):
        client = Client()
        response = client.delete('/books/1/comments?comment_id=1', **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.CDU_6JOu5bOI9SzTF_LRl1I7jso1QxbsiW_-WGrLyAE"})
        
        self.assertEqual(response.status_code, 401)

# 좋아요 뷰
class CommentLikeViewTest(TestCase):
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
        Platform.objects.create(
            id = 1,
            name = 'Kakao'
        )
        User.objects.create(
            id = 1,
            nickname = 'hyun',
            profile_image_url = 'hyun_url1',
            social_id = '1928131461',
            platform_id = 1,
        )
        Comment.objects.create(
            id = 1,
            book_id = 1,
            user_id = 1,
            text = '야호',
            like_count = 1,
            updated_at = '2021.09.29'
        )
    
    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
        Platform.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()
    
    def test_commentlikeview_post_success(self):
        client = Client()
        
        response = client.post('/books/comments-like?comment_id=1', **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"}, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {"MESSAGE": "SUCCESS"}
        )
    
    def test_commentlikeview_post_comment_not_exist(self):
        client = Client()

        response = client.post('/books/comments-like?comment_id=1111', **{"HTTP_Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.qv95Bi-t7XRinlViaIJthSkG5wKt6ZHDICMZm2pANh8"}, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {"MESSAGE": "COMMENT DOES NOT EXIST"}
        )
    
    def test_commentlikeview_post_comment_invalid(self):
        client = Client()

        response = client.post('/books/comments-like?comment_id=1', **{"HTTP_Authorization" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MX0.CDU_6JOu5bOI9SzTF_LRl1I7jso1QxbsiW_-WGrLyAE"}, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)


class SearchViewTest(TestCase):
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
        
        Platform.objects.create(
            id = 1,
            name = 'Kakao'
        )

        User.objects.create(
            id = 1,
            nickname = 'hyun',
            profile_image_url = 'hyun_url1',
            social_id = '1928131461',
            platform_id = 1,
        )

        Comment.objects.create(
            id = 1,
            book_id = 1,
            user_id = 1,
            text = '야호',
            like_count = 1,
            updated_at = '2021.09.29'
        )

    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
        Platform.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_searchview_get_success(self):
        client = Client()
        response = client.get('/books/search?Search_Target=all&target=라면', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
            "RESULT"    : [{
                "title"  : '열두시에 라면을 끓인다는 건',
                "image"  : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                "book_id": 1,
                "author" : ['정다이'],
            }],
            "books_count": 1
            })
    def test_searchview_get_no_result(self):
        client = Client()
        response = client.get('/books/search?Search_Target=all&target=우엑', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {"RESULT": []}
        )

class SearchMainViewTest(TestCase):
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

        Book.objects.create(
            id              = 2,
            title           = '새벽 2시반에 쓰고 있다',
            publish_date    = '2021-09-30',
            description     = '너무 힘들다',
            page            = 123,
            image_url       = 'anything.img',
            publisher_id    = 1,
            book_info_id    = 1
        )

        Category.objects.create(
                id = 1,
                name = '에세이'
            )

        Category.objects.create(
                id = 2,
                name = '자기계발'
            )

        BookCategory.objects.create(
            book_id = 1,
            category_id = 1,
        )

        BookCategory.objects.create(
            book_id = 2,
            category_id = 2,
        )

    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()

    def test_searchmainview_get_success(self):
        client = Client()
        response = client.get('/books/search/Main', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {"RESULT": [
                {
                    "image"   : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                    "category": '에세이'
                },
                {
                    "image"   : 'anything.img',
                    "category": '자기계발'
                }
            ]}
        )
    
class NewBooksViewTest(TestCase):
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

    def test_newbooksview_get_success(self):
        client = Client()
        response = client.get('/books/new?limit=1', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {"RESULT": [
                    {
                        "book_id": 1,
                        "title"  : '열두시에 라면을 끓인다는 건',
                        "image"  : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                        "author" : ['정다이']
                    }
                ]
            }
        )

class MovieRecommendTest(TestCase):
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
        
        Platform.objects.create(
            id = 1,
            name = 'Kakao'
        )

        User.objects.create(
            id = 1,
            nickname = 'hyun',
            profile_image_url = 'hyun_url1',
            social_id = '1928131461',
            platform_id = 1,
        )

        Comment.objects.create(
            id = 1,
            book_id = 1,
            user_id = 1,
            text = '야호',
            like_count = 1,
            updated_at = '2021.09.29'
        )

        Comment.objects.create(
            id = 2,
            book_id = 1,
            user_id = 1,
            text = '새벽 3시다..',
            like_count = 33,
            updated_at = '2021.09.30'
        )

    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
        Platform.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_movierecommend_get_success(self):
        client = Client()
        response = client.get('/books/recommend?limit=1', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {"RESULT": [
                    {
                        "book_image"  : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                        "book_id"     : 1,
                        "title"       : '열두시에 라면을 끓인다는 건',
                        "publish_date": '2019.02.05',
                        "nickname"    : 'hyun', 
                        "user_image"  : 'hyun_url1', 
                        "comment"     : '새벽 3시다..'
                    }
                ]
            }
        )

class BookPublisherViewTest(TestCase):
    def setUp(self):
        Publisher.objects.create(
                id = 1,
                name         = '김영사',
                introduction = '우리는 독자를 섬깁니다.'
        )
        
        BookInfo.objects.create(
                id = 1,
                text = '본문1',
                contents = '목차1'
        )

        BookInfo.objects.create(
                id = 2,
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

        Book.objects.create(
            id              = 2,
            title           = '자고 싶다',
            publish_date    = '2021-09-30',
            description     = '눈이 감긴다',
            page            = 777,
            image_url       = 'anything.img',
            publisher_id    = 1,
            book_info_id    = 2
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

        Author.objects.create(
                id   = 2,
                name = '이무현',
                introduction = '잠 못드는 사람'
            )

        BookAuthor.objects.create(
            id = 1,
            book_id = 1,
            author_id = 1,
        )

        BookAuthor.objects.create(
            id = 2,
            book_id = 2,
            author_id = 2,
        )
    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
        
    def test_bookpublisherview_get_success(self):
        client = Client()
        response = client.get('/books/publisher?search=김영사&limit=2', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {"RESULT":[
                    {
                        "title"  : '열두시에 라면을 끓인다는 건',
                        "image"  : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg',
                        "book_id": 1,
                        "author" : ['정다이']
                    },
                    {
                        "title"  : '자고 싶다',
                        "image"  : 'anything.img',
                        "book_id": 2,
                        "author" : ['이무현']
                    }
                ]
            }
        )

class BookGenreViewTest(TestCase):
    def setUp(self):
        Publisher.objects.create(
                id = 1,
                name         = '김영사',
                introduction = '우리는 독자를 섬깁니다.'
        )
        
        BookInfo.objects.create(
                id = 1,
                text = '본문1',
                contents = '목차1'
        )

        BookInfo.objects.create(
                id = 2,
                text = '본문2',
                contents = '목차2'
        )
        
        BookInfo.objects.create(
                id = 3,
                text = '본문3',
                contents = '목차3'
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

        Book.objects.create(
            id              = 2,
            title           = '자고 싶다',
            publish_date    = '2021-09-30',
            description     = '눈이 감긴다',
            page            = 777,
            image_url       = 'anything.img',
            publisher_id    = 1,
            book_info_id    = 2
        )

        Book.objects.create(
            id              = 3,
            title           = '이제 잘 수 있나',
            publish_date    = '2021-09-30',
            description     = '해치웠나',
            page            = 111,
            image_url       = 'anything2.img',
            publisher_id    = 1,
            book_info_id    = 3
        )

        Category.objects.create(
                id = 1,
                name = '에세이'
            )

        BookCategory.objects.create(
            book_id = 1,
            category_id = 1,
        )

        BookCategory.objects.create(
            book_id = 2,
            category_id = 1,
        )

        BookCategory.objects.create(
            book_id = 3,
            category_id = 1,
        )

        Author.objects.create(
                id   = 1,
                name = '정다이',
                introduction = '''"인생은 사랑이 다야."라고 말하는 로맨티스트.'''
            )

        Author.objects.create(
                id   = 2,
                name = '이무현',
                introduction = '잠 못드는 사람'
            )

        Author.objects.create(
                id   = 3,
                name = '다크써클',
                introduction = '초점이 없어짐'
            )

        BookAuthor.objects.create(
            id = 1,
            book_id = 1,
            author_id = 1,
        )

        BookAuthor.objects.create(
            id = 2,
            book_id = 2,
            author_id = 2,
        )

        BookAuthor.objects.create(
            id = 3,
            book_id = 3,
            author_id = 3,
        )

    def tearDown(self):
        Publisher.objects.all().delete()
        BookInfo.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        BookAuthor.objects.all().delete()
        Category.objects.all().delete()
        BookCategory.objects.all().delete()
    
    def test_bookgenrerview_get_success(self):
        client = Client()
        response = client.get('/books/genre?search=에세이&limit=3', content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {"RESULT":[
                    {
                        "book_id": 1,
                        "title"  : '열두시에 라면을 끓인다는 건',
                        "author" : ['정다이'],
                        "image"  : 'https://image.aladin.co.kr/product/17716/60/cover500/8969523138_1.jpg'    
                    },
                    {
                        "book_id": 2,
                        "title"  : '자고 싶다',
                        "author" : ['이무현'],
                        "image"  : 'anything.img',
                    },
                    {
                        "book_id": 3,
                        "title"  : '이제 잘 수 있나',
                        "author" : ['다크써클'],
                        "image"  : 'anything2.img',
                    }
                ]
            }
        )