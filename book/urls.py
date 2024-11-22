from book import views
from django.urls import path

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('borrow/', views.BorrowBookView.as_view(), name='borrow-book'),
    path('return/', views.ReturnBookView.as_view(), name='return-book'),
    path('borrowed/<int:borrower_id>/', views.BorrowedBooksView.as_view(), name='borrowed-books'),
    path('history/<int:borrower_id>/', views.BorrowerHistoryView.as_view(), name='borrower-history'),
]
