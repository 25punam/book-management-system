from django.contrib import admin
from .models import Book,Borrower,Loan

# Register your models here.
admin.site.register(Book)
admin.site.register(Borrower)
admin.site.register(Loan)