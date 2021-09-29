import json

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Q

from users.decorators import login_decorator
from books.models import (
    BookAuthor, 
    BookCategory, 
    Category, 
    Comment, 
    CommentLike, 
    Book
)


# 상세페이지
class BookDetailView(View):

    def get(self, request, book_id):
        if not Book.objects.filter(id=book_id).exists():
            return JsonResponse({"MESSAGE": "BOOK DOES NOT EXIST"}, status=404)
    
        books = BookAuthor.objects.select_related('book', 'author').filter(book_id=book_id)
        book  = books[0]

        book_list = {
            "title"          : book.book.title,
            "image_url"      : book.book.image_url,
            "book_intro"     : book.book.description,
            "publisher"      : book.book.publisher.name,
            "publisher_intro": book.book.publisher.introduction,
            "book_contents"  : book.book.book_info.contents,
            "pages"          : book.book.page,
            "publish_date"   : book.book.publish_date.strftime("%Y.%m.%d"),
            "authors"        : [book.author.name for book in books],
            "authors_intro"  : [book.author.introduction for book in books],
            "category"       : book.book.category.values()[0]['name']
        }
        
        return JsonResponse({"RESULT": book_list}, status=200)


class CommentView(View):
    # 회원용, 비회원용
    @login_decorator
    def get(self, request, book_id):
        try:
            comments = Comment.objects.select_related('user').filter(book_id=book_id)
            if request.user:
                user_id  = request.user.id
            
                comment_list = [{
                    "nickname"     : comment.user.nickname,
                    "profile_image": comment.user.profile_image_url,
                    "comment"      : comment.text,
                    "comment_id"   : comment.id,
                    "written"      : comment.updated_at.strftime("%Y.%m.%d"),
                    "likes"        : comment.like_count,
                    "liked"        : True if CommentLike.objects.filter(comment_id=comment.id, user_id=user_id).exists() else False,
                    "is_my_comment": True if comment.user_id == int(user_id) else False
                }for comment in comments]
            
            else:
                comment_list = [{
                    "nickname"     : comment.user.nickname,
                    "profile_image": comment.user.profile_image_url,
                    "comment"      : comment.text,
                    "comment_id"   : comment.id,
                    "written"      : comment.updated_at.strftime("%Y.%m.%d"),
                    "likes"        : comment.like_count,
                }for comment in comments]

            return JsonResponse({
                "comments_count": comments.count(),
                "comments": comment_list
            }, status=201)

        except Book.DoesNotExist:
            return JsonResponse({"MESSAGE": "BOOK DOES NOT EXIST"}, status=404)
    
    @login_decorator
    def post(self, request, book_id):
        try:
            data    = json.loads(request.body)
            user_id = request.user.id
            
            Comment.objects.create(
                book_id = book_id,
                user_id = user_id,
                text    = data['text']
            )   
        
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except:
            return JsonResponse({"MESSAGE": "WRONG FORMAT"}, status=401)

    @login_decorator
    def delete(self, request, book_id):
        user_id    = request.user.id
        comment_id = request.GET.get('comment_id', None)
        
        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({"MESSAGE": "COMMENT DOES NOT EXIST"}, status=401)
        comment = Comment.objects.get(id=comment_id)

        if user_id == comment.user_id:
            comment.delete()
        else: 
            return JsonResponse({"MESSAGE": "INVALID USER"}, status=401)
        
        return JsonResponse({"MESSAGE": "SUCCESS"}, status=204)


class CommentLikeView(View):
    # 데코레이터로 id 값 가져와야함
    @login_decorator
    def post(self, request):
        try:
            comment_id     = request.GET.get('comment_id', None)
            user_id        = request.user.id
            target_comment = Comment.objects.get(id=comment_id)
            

            if CommentLike.objects.filter(comment_id=comment_id, user_id=user_id).exists():
                target_comment.like_count -= 1
                CommentLike.objects.filter(comment_id=comment_id, user_id=user_id).delete()
            
            else:   
                CommentLike.objects.create(
                    comment_id = comment_id,
                    user_id = user_id
                )
                target_comment.like_count += 1
                

            target_comment.save()

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        
        except:
            return JsonResponse({"MESSAGE": "COMMENT DOES NOT EXIST"}, status=404)


# 검색창
class SearchView(View):
    
    def get(self, request):
        search_target = request.GET.get('Search_Target', '')
        target        = request.GET.get('target', '')
        
        q = Q()

        search_filter = {
            'all'     : Q(author__name__icontains = target) | Q(category__name__icontains = target) | Q(title__icontains = target),
            'author'  : Q(author__name__icontains = target),
            'category': Q(category__name__icontains = target),
            'title'   : Q(title__icontains = target),
        }

        books = Book.objects.filter(search_filter[search_target]).prefetch_related('author', 'category').distinct()

        if not books:
            return JsonResponse({"RESULT": []},status=200)

        books_list = [{
            "title"  : book.title,
            "image"  : book.image_url,
            "book_id": book.id,
            "author" : [author.name for author in book.author.all()],
        }for book in books]

        return JsonResponse({
            "RESULT"    : books_list,
            "books_count": len(books)
            }, status=200)


# 검색창 메인페이지(카테고리 별 image 가져오기)
class SearchMainView(View):
    def get(self, request):
        try:
            categories = Category.objects.all()
            book       = BookCategory.objects.select_related('book', 'category')
            
            category_list = [{
                "image"   : book.filter(category__name=category.name).first().book.image_url if book.filter(category__name=category.name).exists() else "NO IMAGE",
                "category": category.name
            }for category in categories]

            return JsonResponse({"RESULT": category_list}, status=200)

        except:
            return JsonResponse({"MESSAGE": "NO DATA"}, status=404)


# 메인페이지 1       
class NewBooksView(View):
    def get(self, request):
        
        OFFSET = 0
        LIMIT  = request.GET.get('limit', '')

        books  = Book.objects.all().order_by('-publish_date')

        if LIMIT == '':
            LIMIT = len(books)
        else:
            LIMIT = int(LIMIT)

        book_list = [{
            "book_id": book.id,
            "title"  : book.title,
            "image"  : book.image_url,
            "author" : [author.name for author in book.author.all()],
        }for book in books]

        return JsonResponse({"RESULT": book_list[OFFSET:LIMIT]}, status=200)


# 메인 페이지 2
class MovieRecommend(View):
    def get(self, request):
        
        OFFSET = 0
        LIMIT  = request.GET.get('limit', '')
        books  = Book.objects.prefetch_related('comment_set').order_by('-publish_date')
        
        if LIMIT == '':
            LIMIT = len(books)
        else:
            LIMIT = int(LIMIT)

        book_list = [{
            "book_image"  : book.image_url,
            "book_id"     : book.id,
            "title"       : book.title,
            "publish_date": book.publish_date.strftime("%Y.%m.%d"),
            "nickname"    : book.comment_set.order_by('like_count').first().user.nickname if Comment.objects.filter(book_id=book.id).exists() else "NONE", 
            "user_image"  : book.comment_set.order_by('like_count').first().user.profile_image_url if Comment.objects.filter(book_id=book.id).exists() else "NONE", 
            "comment"     : book.comment_set.order_by('like_count').first().text if Comment.objects.filter(book_id=book.id).exists() else "NONE",
        }for book in books]

        return JsonResponse({"RESULT": book_list[OFFSET:LIMIT]}, status=200)


# 메인페이지 #3
class BookPublisherView(View):
    def get(self, request):
        publisher = request.GET.get('search', '')
        LIMIT = request.GET.get('limit', '')
        OFFSET = 0

        q = Q()

        if publisher:
            q = Q(publisher__name=publisher)
        
        books  = Book.objects.select_related('publisher').filter(q)

        if LIMIT == '':
            LIMIT = len(books)
        else:
            LIMIT = int(LIMIT)

        publish_list = [{
            "book_title": book.title,
            "book_image": book.image_url,
            "book_id"   : book.id,
            "author" : [author.name for author in book.author.all()],
        }for book in books]
        
        return JsonResponse({"RESULT":publish_list[OFFSET:LIMIT]}, status=200)


# 메인페이지 #4
class BookGenreView(View):

    def get(self, request):
        genre = request.GET.get('search', '')
        LIMIT = request.GET.get('limit', '')
        OFFSET = 0

        q = Q()
        
        if genre:
            q = Q(category__name=genre)

        books = Book.objects.filter(q).prefetch_related('author')
        
        if LIMIT == '':
            LIMIT = len(books)
        else:
            LIMIT = int(LIMIT)

        book_list = [{
            "book_id": book.id,
            "title" : book.title,
            "author": [author.name for author in book.author.all()],
            "image" : book.image_url,
        }for book in books]
            
        return JsonResponse({"RESULT": book_list[OFFSET:LIMIT]}, status=201)


