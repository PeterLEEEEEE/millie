import json

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Q

from books.models import (
    BookAuthor, 
    BookCategory, 
    Category, 
    Comment, 
    CommentLike, 
    Book
)
from books.utils  import query_debugger


# 상세페이지
class BookDetailView(View):
    @query_debugger
    def get(self, request, book_id):
        # 
        if not Book.objects.filter(id=book_id).exists():
            return JsonResponse({"MESSAGE": "BOOK DOES NOT EXIST"}, status=404)
        
        books = BookAuthor.objects.select_related('book', 'author').filter(book_id=book_id)
        book = books[0]

        book_list = {
            "title": book.book.title,
            "image_url": book.book.image_url,
            "publisher": book.book.publisher.name,
            "publisher_intro": book.book.publisher.introduction,
            "pages": book.book.page,
            "publish_date": book.book.publish_date,
            "authors": [book.author.name for book in books],
            "authors_intro": [book.author.introduction for book in books],
            "category": book.book.category.values()[0]['name']
        }
        
        return JsonResponse({"MESSAGE": book_list}, status=200)


class CommentView(View):
    @query_debugger
    def get(self, request, book_id):
        comments = Comment.objects.select_related('user').filter(book_id=book_id)
        
        comment_list = [{
            "nickname": comment.user.nickname,
            "profile_image": comment.user.profile_image_url,
            "comment": comment.text,
            "written": comment.updated_at.strftime("%Y.%m.%d"),
            "likes": comment.like_count,
            #"likes": CommentLike.objects.filter(comment_id=comment.id).count()
        }for comment in comments]
        
        return JsonResponse({
            "comments_count": comments.count(),
            "comments": comment_list
        }, status=201)

    def post(self, request, book_id):
        try:
            data = json.loads(request.body)
            user_id = request.GET.get('id', None) # 추후 소셜 로그인 완료시 수정
            
            Comment.objects.update_or_create(
                book_id = book_id,
                user_id = user_id,
                defaults = {'text': data['text']} 
            )   
        
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "WRONG FORMAT"}, status=401)

    def delete(self, request):
        user_id = request.user.id
        comment_id = request.GET.get('id', None)
        
        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({"MESSAGE": "COMMENT DOES NOT EXIST"})
        comment = Comment.objects.get(id=comment_id)

        if user_id == comment.user_id:
            comment.delete()
        
        return JsonResponse({"MESSAGE": "SUCCESS"}, status=204)

# class CommentDeleteView(View):
#     # @login_decorator 
#     def post(self, request, comment_id):
        
#         Comment.objects.filter(id=comment_id).delete()

#         return JsonResponse({"messge": "SUCCESS"}, status=201)

class CommentLikeView(View):
    # 데코레이터로 id 값 가져와야함
    @query_debugger
    def post(self, request):
        try:
            comment_id = request.GET.get('comment_id', None)
            user_id = request.GET.get('id', None)
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

            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except:
            return JsonResponse({"MESSAGE": "COMMENT DOES NOT EXIST"}, status=404)

# 검색창
class SearchView(View):
    @query_debugger
    def get(self, request):
        search_target = request.GET.get('Search_Target', '')
        target = request.GET.get('target', '')
        q = Q()

        search_filter = {
            'all'     : Q(author__name__icontains = target) | Q(category__name__icontains = target) | Q(title__icontains = target),
            'author'  : Q(author__name__icontains = target),
            'category': Q(category__name__icontains = target),
            'title'   : Q(title__icontains = target),
        }

        books = Book.objects.filter(search_filter[search_target]).prefetch_related('author', 'category').distinct()

        if not books:
            return JsonResponse({"MESSAGE": "BOOK NOT FOUND"},status=404)

        books_list = [{
            "title": book.title,
            "image": book.image_url,
            "author": [author.name for author in book.author.all()],
        }for book in books]

        return JsonResponse({
            "MESSAGE": books_list,
            "books_count": len(books)
            }, status=200)


# 검색창 메인페이지(카테고리 별 image 가져오기)
class SearchMainView(View):
    def get(self, request):
        categories = Category.objects.all()
        book = BookCategory.objects.select_related('book', 'category')
        
        category_list = [{
            "image": book.filter(category__name=category.name).first().book.image_url if book.filter(category__name=category.name).exists() else "NO IMAGE",
            "category": category.name
        }for category in categories]

        return JsonResponse({"MESSAGE": category_list}, status=200)


# 메인페이지 1       
class NewBooksView(View):
    def get(self, request):
        '''
        1) 최신 업데이트 순(order by --> limit: 20)
        '''
        OFFSET = request.GET.get('OFFSET', 0)
        LIMIT = 20

        books = Book.objects.all().order_by('-publish_date')

        book_list = [{
            "title": book.title,
            "image": book.image_url,
            "pages": book.page,
        }for book in books][OFFSET:OFFSET+LIMIT]

        return JsonResponse({"BOOKS": book_list}, status=200)


# 메인 페이지 2
class MovieRecommend(View):
    @query_debugger
    def get(self, request):
        # annotation(like=Max(likes))??
        # 책은 날짜 순으로 가져옴 .first()?
        '''
        return: 
            book_image
            most_liked_comment, commenter's nickname
            order_by publish_date
        '''
        OFFSET = 0
        LIMIT = request.GET.get('limit', 20)
        books = Book.objects.prefetch_related('comment_set').order_by('-publish_date')
        
        book_list = [{
            "book_image": book.image_url,
            "title": book.title,
        #     "nickname": book.comment_set.order_by('like_count').first().user.nickname if Comment.objects.filter(book_id=book.id).exists() else "NONE", 
        #     "user_image": book.comment_set.order_by('like_count').first().user.profile_image_url if Comment.objects.filter(book_id=book.id).exists() else "NONE", 
        #     "comment": book.comment_set.order_by('like_count').first().text if Comment.objects.filter(book_id=book.id).exists() else "NONE",
        }for book in books][OFFSET:LIMIT]

        return JsonResponse({"book": book_list}, status=200)

# 메인페이지 #3
class BookPublisherView(View):
    def get(self, request):
        publisher = request.GET.get('publisher', '')
        OFFSET = 0
        LIMIT = 10

        q = Q()

        if publisher:
            q = Q(publisher__name=publisher)
        
        books = Book.objects.select_related('publisher').filter(q)

        publish_list = [{
            "book_title": book.title,
            "book_image": book.image_url,
        }for book in books]
        
        return JsonResponse({"MESSAGE":publish_list}, status=200)


# 메인페이지 #4
class BookGenreView(View):
    @query_debugger
    def get(self, request):
        genre = request.GET.get('genre', '')
        LIMIT = request.GET.get('limit', '')
        OFFSET = 0

        q = Q()
        
        if genre:
            q = Q(category__name=genre)

        books = Book.objects.filter(q).prefetch_related('author')
        
        if LIMIT == '':
            LIMIT = len(books)
        
        book_list = [{
            "title": book.title,
            "author": book.author.values()[0]['name'],
            "image": book.image_url,
        }for book in books][OFFSET:LIMIT]
            
        return JsonResponse({"Books": book_list}, status=201)


