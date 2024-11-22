
# Library Management System

## Project Overview
This project is a Django-based API for managing a library's book borrowing system. It allows users to manage books, handle borrow and return operations, and track borrower history while adhering to specific rules such as borrowing limits and membership status.

## Features

### Book Management

#### **Add New Books**  
- **Endpoint**: `POST /books/`  
  Add a new book to the system.  

#### **List All Books**  
- **Endpoint**: `GET /books/`  
  Retrieve a list of all books, with an optional filter for availability using `?available=true`.  
  **Query Parameters**:  
  - `available`: Optional filter, set to `true` or `false` to show available/unavailable books.

---

### Borrowing and Returning Books

#### **Borrow a Book**  
- **Endpoint**: `POST /borrow/`  
  Borrow a book using `book_id` and `borrower_id`. This updates the book's availability and increments its borrow count.  


