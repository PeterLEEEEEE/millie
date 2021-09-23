from django.db import models

from users.models import User
# from books.models import Shelf
from core.models import TimeStamp


class Library(TimeStamp):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    favorite = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)
    current_page = models.IntegerField() 
    book = models.ManyToManyField("books.Book", through="LibraryBook")
    
    class Meta:
        db_table = "libraries"


class LibraryBook(models.Model):
    book    = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    library = models.ForeignKey("Library", on_delete=models.CASCADE)
    shelf   = models.ForeignKey("books.Shelf", on_delete=models.CASCADE)

    class Meta:
        db_table = "library_books"