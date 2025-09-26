# smart_expense_tracker_project


Setup Instructions:

1- Clone the repository
  git clone https://github.com/Musthak-PT/smart_expense_tracker_project.git
  cd smart_expense_tracker_project


2️- Backend Setup (Django REST Framework)

  Create a virtual environment
      python -m venv venv
  
  Activate the virtual environment
  
  Windows:
    venv\Scripts\activate
    
  Linux/macOS:
    source venv/bin/activate

3- Install Python dependencies

  pip install -r requirements.txt

4-Apply database migrations
  python manage.py makemigrations
  python manage.py migrate


5-Create a superuser (optional, for admin panel)
  python manage.py createsuperuser

6-Run the Django development server
  python manage.py runserver 9001(port)
  ackend will now be accessible at http://127.0.0.1:9001/



Design Choices:

  1- Database Schema:
  
  User: 
    Uses Django’s built-in User model for authentication and identification. This avoids reinventing authentication and leverages Django’s secure password              hashing.
  
  Category:
    Stores expense categories (name). Categories are shared across all users for simplicity and consistency.
  
  Expense: 
    Each expense is linked to a User and a Category, with fields for amount, description, and date.
  
  user → ForeignKey to User ensures each expense belongs to a specific user.
  category → ForeignKey to Category, with SET_NULL on deletion to keep past expenses intact.
  amount → DecimalField with max_digits=10 and decimal_places=2 ensures precision for monetary values.
  date → Used for filtering by month/year in reports.
  
  Constraints:
    Foreign keys enforce referential integrity.
    NOT NULL constraints for essential fields like user and amount.
    Ordering: Expenses are ordered by -date by default for easier listing of recent entries


2️- SQL Query for Monthly Summary:

  The monthly summary aggregates a user’s expenses by category and provides a total expense for a given month.
  
  Django ORM implementation:
   expenses_by_category = expenses.values(
        category_name=F('category__name')
    ).annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')

3️- Additional Design Choices:
  Nested serialization: Expenses include full user and category details in responses for easier frontend rendering.
  
  JWT Authentication: Protects all API endpoints and eliminates the need to pass user_id in requests, enhancing security.
  
  Modular API design: Separate endpoints for Users, Categories, Expenses, and Reports allow scalability and easy maintenance.
  
  Optional Full CRUD: Supports update and deletion of expenses for complete user control.


📌 API Documentation:
  
  1. Users:
     
      ➤ Create User
      
      POST http://127.0.0.1:9001/api/users
      
      Payload
      
      {
        "username": "alice",
        "password": "password123",
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Wonder"
      }
      
      ➤ List Users
      
      GET http://127.0.0.1:9001/api/users
      
      Response
      
      [
        {
          "id": 1,
          "username": "admin",
          "first_name": "",
          "last_name": "",
          "email": "admin@gmail.com"
        },
        {
          "id": 2,
          "username": "alice",
          "first_name": "Alice",
          "last_name": "Wonder",
          "email": "alice@example.com"
        }
      ]
      
      ➤ Get JWT Token
      
      POST http://127.0.0.1:9001/api/token/
      
      Payload
      
      {
        "username": "alice",
        "password": "password123"
      }
      
      
      Response
      
      {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
      }
      
      ➤ Refresh Access Token
      
      POST http://127.0.0.1:9001/api/token/refresh/
      
      Payload
      
      {
        "refresh": "<refresh_token>"
      }
      
      
      Response
      
      {
        "access": "<access_token>"
      }
  
  2. Categories
      ➤ Create Category
      
      POST http://127.0.0.1:9001/api/categories
      
      Payload
      
      {
        "name": "Transportation"
      }
      
      ➤ List Categories
      
      GET http://127.0.0.1:9001/api/categories
      
      Response
      
      [
        {
          "id": 1,
          "name": "Groceries"
        },
        {
          "id": 2,
          "name": "Electricity"
        },
        {
          "id": 3,
          "name": "Transportation"
        }
      ]
  
  3. Expenses:
      ➤ Create Expense
      
      POST http://127.0.0.1:9001/api/expenses
      Authorization: Bearer <access_token>
      
      Payload
      
      {
        "category_id": 1,
        "amount": "150.50",
        "description": "Weekly groceries",
        "date": "2025-09-26"
      }
      
      ➤ List Expenses
      
      GET http://127.0.0.1:9001/api/expenses
      
      Response
      
      [
        {
          "id": 1,
          "user": {
            "id": 2,
            "username": "alice",
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
          },
          "category": {
            "id": 1,
            "name": "Groceries"
          },
          "amount": "150.50",
          "description": "Weekly groceries",
          "date": "2025-09-26"
        }
      ]
      
      ➤ Retrieve Single Expense
      
      GET http://127.0.0.1:9001/api/expenses/<id>
      
      Response
      
      {
        "id": 2,
        "user": {
          "id": 2,
          "username": "alice",
          "first_name": "Alice",
          "last_name": "Wonder",
          "email": "alice@example.com"
        },
        "category": {
          "id": 2,
          "name": "Electricity"
        },
        "amount": "150.50",
        "description": "Weekly transp",
        "date": "2025-09-26"
      }
      
      ➤ Update Expense
      
      PUT http://127.0.0.1:9001/api/expenses/<id>
      
      Payload
      
      {
        "category_id": 2,
        "amount": "200.00",
        "description": "Updated grocery shopping",
        "date": "2025-09-27"
      }
      
      
      Response
      
      {
        "id": 1,
        "user": {
          "id": 2,
          "username": "alice",
          "first_name": "Alice",
          "last_name": "Wonder",
          "email": "alice@example.com"
        },
        "category": {
          "id": 2,
          "name": "Electricity"
        },
        "amount": "200.00",
        "description": "Updated grocery shopping",
        "date": "2025-09-27"
      }
      
      ➤ Delete Expense
      
      DELETE http://127.0.0.1:9001/api/expenses/<id>
  
  4. Monthly Summary Report:
  
      GET http://127.0.0.1:9001/api/reports/monthly_summary?year=2025&month=09&user_id=1
      
      Response:
          {
        "total_expenses": 571.25,
        "expenses_by_category": [
          { "category_name": "Groceries", "total_amount": 450.75 },
          { "category_name": "Utilities", "total_amount": 120.50 }
        ]
      }


Discussion Questions
  Low Complexity
  
  1. Why did you choose a DECIMAL or NUMERIC type for the amount column instead of FLOAT?
  
    DECIMAL ensures precise representation of monetary values, avoiding rounding errors that occur with FLOAT.
    FLOAT uses binary floating-point representation, which can lead to inaccuracies in calculations for financial data.
    Using DECIMAL guarantees correct totals and aggregates for reports and user expenses.
  
  2. What is the purpose of a foreign key constraint?
  
  Enforces referential integrity, ensuring that related data exists.
  
  Example: An Expense must be linked to a valid User and optionally to a valid Category.
  
  Helps prevent orphaned records and maintains database consistency.
  
  Medium Complexity
  
  3. The current design requires passing a user_id with each request. What are the security drawbacks of this method, and what would be a more robust authentication system to implement?
  
  Drawbacks: Users could maliciously pass another user’s ID to access or manipulate their data.
  
  Solution: Implement JWT-based authentication. Each request uses a token, and the backend derives the current user from the token (request.user).
  
  This removes the need to pass user_id in query params and prevents unauthorized access.
  
  4. What are the benefits of handling the report aggregation in the database (with SQL) versus in the backend (with Python)?
  
  Efficiency: SQL aggregation uses the database engine, which is optimized for large-scale data operations.
  
  Reduced memory usage: Only aggregated results are sent to the backend, rather than all rows.
  
  Simpler code: Backend logic stays clean; less custom looping or summing required.
  
  Scalability: Handles millions of rows without impacting backend performance.
  
  High Complexity
  
  5. If the expenses table grew to millions of records, what steps would you take to ensure the monthly summary report remains fast for all users?
  
  Add indexes on user_id and date columns to speed up filtering.
  
  Use database-level aggregation instead of fetching all rows.
  
  Implement caching (Redis or in-memory cache) for frequently requested monthly reports.
  
  Partition the table by date or user if dataset grows extremely large.
  
  Consider denormalized summary tables updated via triggers or scheduled jobs.
  
  6. How would you design a "budgeting" feature where a user can set a monthly spending limit for a specific category (e.g., "$500 for Groceries")? Describe the necessary database changes and API endpoints.
  
  Database changes:
  
  New model Budget with fields: user (FK), category (FK), month, year, limit_amount.
  
  API endpoints:
  
  POST /api/budgets → Create a budget for a user/category/month.
  
  GET /api/budgets?user_id=<id>&month=MM&year=YYYY → Fetch budget info.
  
  Optional: PUT /api/budgets/<id> and DELETE /api/budgets/<id> for update/delete.
  
  Logic:
  
  On monthly summary, calculate total expenses per category and compare against the budget.
  
  Send alerts or warnings if the user exceeds the set limit.

