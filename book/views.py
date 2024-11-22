from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer
from rest_framework.views import APIView
from django.utils.timezone import now

class BookListView(APIView):
    """
    View for listing all books and adding a new book.

    GET: Retrieves a list of books. Optionally filter by availability using the 'available' query parameter.
    POST: Creates a new book entry with the data provided in the request body.
    """
    def get(self, request):
        available = request.GET.get('available')
        if available is not None:
            books = Book.objects.filter(available=available.lower() == 'true')
        else:
            books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new book in the database.
        
        If the provided data is valid, it saves the book and returns a 201 Created response.
        Otherwise, returns a 400 Bad Request with the validation errors.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BorrowBookView(APIView):
    """
    View for borrowing a book.

    POST: Allows a borrower to borrow a book, updating the availability of the book and
    incrementing the borrow count. It also checks the borrower's status and borrowing limit.
    """
    def post(self, request):
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')

        book = get_object_or_404(Book, id=book_id)
        borrower = get_object_or_404(Borrower, id=borrower_id)

        if not borrower.is_active:
            return Response(
                {"error": "Borrower is not active."},
                status=status.HTTP_403_FORBIDDEN
            )
        if Loan.objects.filter(borrower=borrower, is_returned=False).count() >= 3:
            return Response(
                {"error": "Borrower has reached the borrowing limit of 3 books."},
                status=status.HTTP_403_FORBIDDEN
            )
        if not book.available:
            return Response(
                {"error": "Book is not available for borrowing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan = Loan.objects.create(book=book, borrower=borrower)
        book.available = False
        book.borrow_count += 1
        book.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReturnBookView(APIView):
    """
    View for returning a borrowed book.

    POST: Updates the loan record when a book is returned. Marks the book as available again and sets the
    loan's return status to True.
    """
    def post(self, request):
        book_id = request.data.get('book_id')

        book = get_object_or_404(Book, id=book_id)
        loan = get_object_or_404(Loan, book=book, is_returned=False)

        loan.is_returned = True
        loan.return_date = now()
        loan.save()

        book.available = True
        book.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)


class BorrowedBooksView(APIView):
    """
    View for listing all active borrowed books for a specific borrower.

    GET: Retrieves all books that a borrower currently has out on loan and has not returned yet.
    """
    def get(self, request, borrower_id):
        borrower = get_object_or_404(Borrower, id=borrower_id)
        loans = Loan.objects.filter(borrower=borrower, is_returned=False)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


class BorrowerHistoryView(APIView):
    """
    View for listing all borrowed books of a specific borrower, including returned books.

    GET: Retrieves the borrowing history of a borrower, showing both active and returned loans.
    """
    def get(self, request, borrower_id):
        borrower = get_object_or_404(Borrower, id=borrower_id)
        loans = Loan.objects.filter(borrower=borrower)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)