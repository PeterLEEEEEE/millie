from core.models import TimeStamp
from django.db import models

from users.models import User
from libraries.models import LibraryBook, Library


class Book(TimeStamp):
    title        = models.CharField(max_length = 200)
    publish_date = models.DateField()
    description  = models.CharField(max_length = 1000)
    page         = models.IntegerField()
    image_url    = models.CharField(max_length = 500)
    publisher    = models.ForeignKey("Publisher", on_delete = models.CASCADE)
    book_info    = models.ForeignKey("BookInfo", on_delete=models.CASCADE)
    category     = models.ManyToManyField("Category", through = "BookCategory")
    author       = models.ManyToManyField("Author", through = "BookAuthor")
    user_comment = models.ManyToManyField(User, through = "Comment")
    

    class Meta:
        db_table = "books"

class BookInfo(TimeStamp):
    text = models.TextField()
    contents = models.CharField(max_length=300)
    
    class Meta:
        db_table = "book_infos"


class Publisher(models.Model):
    name         = models.CharField(max_length = 45)
    introduction = models.TextField()

    class Meta:
        db_table = "publishers"

class Category(TimeStamp):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = "categories"

class BookCategory(models.Model):
    book     = models.ForeignKey("Book", on_delete = models.CASCADE)
    category = models.ForeignKey("Category", on_delete = models.CASCADE)

    class Meta:
        db_table = "book_categories"

class Author(TimeStamp):
    name         = models.CharField(max_length = 45)
    introduction = models.TextField()

    class Meta:
        db_table = "authors"

class BookAuthor(models.Model):
    book   = models.ForeignKey("Book", on_delete = models.CASCADE)
    author = models.ForeignKey("Author", on_delete = models.CASCADE)

    class Meta:
        db_table = "book_authors"

class Shelf(TimeStamp):
    name    = models.CharField(max_length = 45)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    book    = models.ManyToManyField('Book', through = LibraryBook)

    class Meta:
        db_table = "shelves"


class Comment(TimeStamp):
    book      = models.ForeignKey("Book", on_delete = models.CASCADE)
    user      = models.ForeignKey("users.User", on_delete = models.CASCADE)
    text      = models.CharField(max_length = 500)
    like_count = models.PositiveIntegerField(default=0)
    user_like = models.ManyToManyField("users.User", through = "CommentLike", related_name = "like")

    class Meta:
        db_table = "comments"

class CommentLike(TimeStamp):
    comment = models.ForeignKey("Comment", on_delete = models.CASCADE)
    user    = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        db_table = "comment_likes" 
