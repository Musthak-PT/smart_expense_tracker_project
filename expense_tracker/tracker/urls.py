# tracker/urls.py
from django.urls import path
from .views import (
    UserListCreateView,
    CategoryListCreateView,
    ExpenseListCreateView,
    ExpenseRetrieveUpdateDestroyView,MonthlySummaryView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('users', UserListCreateView.as_view(), name='users'),

    # Categories
    path('categories', CategoryListCreateView.as_view(), name='categories'),

    # Expenses
    path('expenses', ExpenseListCreateView.as_view(), name='expenses'),
    path('expenses/<int:pk>', ExpenseRetrieveUpdateDestroyView.as_view(), name='expense-detail'),
    path('reports/monthly_summary', MonthlySummaryView.as_view(), name='monthly-summary'),
]
