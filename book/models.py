
from django.db import models
from django.utils.timezone import now

class Book(models.Model):
    """
    Represents a book in the library.

    Fields:
    - title: The title of the book.
    - author: The author of the book.
    - borrow_count: The number of times the book has been borrowed.
    - available: A boolean indicating whether the book is available for borrowing.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    borrow_count = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Borrower(models.Model):
    """
    Represents a borrower in the library system.

    Fields:
    - name: The name of the borrower.
    - email: The borrower's email address (unique).
    - is_active: A boolean indicating whether the borrower is active and allowed to borrow books.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    """
    Represents a loan of a book to a borrower.

    Fields:
    - book: A foreign key linking to the Book model.
    - borrower: A foreign key linking to the Borrower model.
    - borrow_date: The date and time when the book was borrowed.
    - return_date: The date and time when the book was returned (nullable).
    - is_returned: A boolean indicating whether the book has been returned.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=now)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} loaned by {self.borrower.name}"
