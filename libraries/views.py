import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from users.decorators import login_decorator
from books.models import Author, Book, Shelf
from libraries.models import LibraryBook, Library

# [POST] 127.0.0.1:8000/libraries - 책장추가기능(서재페이지) --> input : "shelf_name" / 예외처리 : 빈값입력(인풋에러) & 입력중복(중복에러) & 키값에러(키에러) 
class LibraryView(View):    # [branch]feature/library 
    @login_decorator
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            shelf_name = data["shelf_name"]
            user_library = Library.objects.get(user_id=request.user.id)
            
            if not shelf_name:
                return JsonResponse({"MESSAGE": "INPUT ERROR"}, status=404)

            if Shelf.objects.filter(library_id=user_library.id, name=shelf_name).exists():
                return JsonResponse({"MESSAGE": "ALREADY EXISTED SHELF"}, status=404)

            Shelf.objects.create(
                name = data["shelf_name"],
                library_id = user_library.id
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

# [GET] 127.0.0.1:8000/libraries - 전체도서(서재페이지) --> input : "shelf_name" / 예외처리 : 키값에러(키에러) & 없는 유저(do not exist)
    @login_decorator
    def get(self, request):
        try:
            user         = User.objects.get(id=request.user.id)           
            user_library = Library.objects.get(user_id=request.user.id)
            totalbooks   = user_library.librarybook_set.all()

            totalbook_list = []
            results = [{
                "user_nickname" : user.nickname,
                "user_image"    : user.profile_image_url,
                "user_totalbooks" : totalbook_list,
            }]

            double_check_list = []

            for books in totalbooks :           
                bookauthor = books.book.bookauthor_set.all().values()
                book_author = Author.objects.get(id=bookauthor[0]['author_id']).name
            
                if books.book_id not in double_check_list:
                    totalbook_list.append({    
                        "book_id"           : books.book_id,
                        "book_name"         : books.book.title,
                        "book_image"        : books.book.image_url,
                        "book_author"       : book_author,
                        "book_current_page" : books.current_page,      
                        "book_publish_date" : books.book.publish_date,
                        "book_publisher"    : books.book.publisher.name,        
                        "favorite"          : books.favorite
                    })
                    double_check_list.append(books.book_id)
            
            return JsonResponse({"results": results}, status=200)
            
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "User Does Not Exists"}, status=404)


# [GET] 127.0.0.1:8000/libraries/shelf - 책장 별 도서 (서재페이지) / 예외처리 : 키값에러(키에러) & 없는 유저(do not exist)
class ShelfView(View):
    @login_decorator
    def get(self, request):
        try:
            user         = User.objects.get(id=request.user.id)
            user_library = Library.objects.get(user_id=request.user.id)
            shelves      = Shelf.objects.filter(library_id=user_library.id)
            librarybooks = LibraryBook.objects.select_related('book','shelf').filter(library_id=user_library.id)
            
            shelves_list = []
            results = [{
                "user_nickname" : user.nickname,
                "user_image"    : user.profile_image_url,
                "user_shelves"  : shelves_list,
            }]

            readingbooks_list = []
            shelves_list.append({
                        "shelf_name":  "읽고있는 책",
                        "book_image" : readingbooks_list
                    })

            double_check_list =[]
            for books in librarybooks :
                if books.reading == True and books.book.image_url not in double_check_list:
                    readingbooks_list.append(books.book.image_url)
                    double_check_list.append(books.book.image_url)

            favoritebooks_list = []
            shelves_list.append({
                "shelf_name":  "My Favorite",
                "book_image" : favoritebooks_list
            })

            double_check_list =[]
            for books in librarybooks:
                if books.favorite == True and books.book.image_url not in double_check_list:
                    favoritebooks_list.append(books.book.image_url)
                    double_check_list.append(books.book.image_url)

            for shelf in shelves:
                book_list = []
                shelves_list.append({
                    "shelf_id" : shelf.id,
                    "shelf_name":  shelf.name,
                    "book_image" : book_list
                })
            
                library = librarybooks.filter(shelf_id = shelf.id)
                for books in library:
                    book_list.append(books.book.image_url)

            return JsonResponse({"results": results}, status=200)
            
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "User Does Not Exists"}, status=404)


# [POST] 127.0.0.1:8000/libraries/shelfdelete - 책장삭제기능(서재페이지) --> input : "shelf_id" / 예외처리 : 빈값입력(인풋에러) & 키값에러(키에러)         
class ShelfDeleteView(View):        #[branch] feature/shelfdelete
    @login_decorator 
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            shelf_id = data["shelf_id"]

            if not shelf_id:
                return JsonResponse({"MESSAGE": "INPUT ERROR"}, status=404)

            user_library = Library.objects.get(user_id=request.user.id)
            user_librarybooks = user_library.shelf_set.all().filter(id=shelf_id)
            user_librarybooks.delete()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)


# [POST] 127.0.0.1:8000/libraries/shelflist - 책 추가 기능 --> input : "book_id" , "shelf_id"/ 예외처리 : 빈값입력(인풋에러) & 입력중복(중복에러) & 키값에러(키에러)  
class ShelfListView(View):      #[branch] feature/shelflist
    @login_decorator
    def post(self, request, **kwargs):
        try: 
            data = json.loads(request.body)
            shelf_id = data["shelf_id"]  
            book_id = data["book_id"]      
            user_library = Library.objects.get(user_id=request.user.id)

            if not shelf_id:
                return JsonResponse({"MESSAGE": "SHELF ERROR"}, status=404)

            if not book_id:
                return JsonResponse({"MESSAGE": "BOOK ERROR"}, status=404)
            
            if LibraryBook.objects.filter(book_id=book_id, shelf_id=shelf_id).exists():
                    return JsonResponse({"MESSAGE": "ALREADY EXISTED BOOK IN SHELF"}, status=404)

            LibraryBook.objects.create(
                book_id = book_id,
                library_id = user_library.id,
                shelf_id = shelf_id,
                favorite = False,
                reading = False,
                current_page = 0,
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)
# [GET] 127.0.0.1:8000/libraries/shelflist - 책장조회 기능 
    @login_decorator
    def get(self, request):
        user         = User.objects.get(id=request.user.id)    
        user_library = Library.objects.get(user_id=request.user.id)   

        totalshelves   = user_library.shelf_set.all()

        shelves_list = [{
            "shelf_id"  : shelf.id,
            "shelf_name" : shelf.name
            }for shelf in totalshelves ]

        results = [{
            "user_nickname" : user.nickname,
            "user_image"    : user.profile_image_url,
            "shelves_name"  : shelves_list
        }]
        return JsonResponse({"results": results}, status=200)

# [GET] 127.0.0.1:8000/libraries/1- 도서별 유저조회(상세페이지) --> input : url정보 참고 "book_id"
class LibraryListView(View):        #[branch] feature/librarylist
    def get(self, request, book_id):
        librarybook = LibraryBook.objects.filter(book_id = book_id)

        double_check_list = []
        list = []
        for id in librarybook:
            if id.library_id not in double_check_list:
                list.append(id.library_id)
                double_check_list.append(id.library_id)
        
        results=[]
        results.append({"total_library_count" : len(list)})

        for user_id in list:
            user_library = Library.objects.get(id=user_id)
            results.append({
                "user_nickname" : user_library.user.nickname,
                "user_url" : user_library.user.profile_image_url
            })
        return JsonResponse({"results": results}, status=200)

class ViewerView(View):
    @login_decorator
    def get(self, request, book_id):
        if request.user:
            library_book = LibraryBook.objects.select_related('book', 'library', 'book__book_info').filter(library__user = request.user, book__id=book_id).prefetch_related('book__author')

            result = [{
                'book_id' : library.book.id,
                'title' : library.book.title,
                'author' : [author.name for author in library.book.author.all()],
                'book_info' : library.book.book_info.contents,
                'image_url' : library.book.image_url,
                'current_page' : library.current_page,
                's3_url' : library.book.book_info.text
            }for library in library_book]

            return JsonResponse({'RESULT' : result}, status = 200)
        
        else:
            return JsonResponse({'MESSAGE' : "WRONG_FORMAT"}, status = 401)


