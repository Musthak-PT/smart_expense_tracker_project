# tracker/views.py
from rest_framework import generics, status , permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer , UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------- Users ----------------
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # allow registration without login


#Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

#Expenses: list/create for authenticated users; list can be filtered by ?user_id (optional)
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # If admin or normal user, default behavior: list all expenses for the authenticated user
        # Optional: Accept query param user_id only if request.user.is_staff (for admin viewing others)
        user_param = self.request.query_params.get('user_id')
        if user_param and self.request.user.is_staff:
            return Expense.objects.filter(user_id=user_param).order_by('-date')
        # Default: show the authenticated user's expenses
        if self.request.user.is_authenticated:
            return Expense.objects.filter(user=self.request.user).order_by('-date')
        # Not authenticated => empty
        return Expense.objects.none()

    def perform_create(self, serializer):
        # Save expense with the authenticated user
        serializer.save(user=self.request.user)


# --- Expense detail (retrieve, update, delete)
class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Ensure the owner remains the same. We don't allow changing .user via update.
        serializer.save(user=self.request.user)
        
# monthly summary CBV

class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Read query params
        user_id = request.query_params.get('user_id')
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        # Validate inputs
        if not all([user_id, year, month]):
            return Response({"error": "user_id, year, and month are required"}, status=400)

        try:
            user_id = int(user_id)
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "user_id, year, and month must be integers"}, status=400)

        # Filter expenses by user, year, and month
        expenses = Expense.objects.filter(
            user_id=user_id,
            date__year=year,
            date__month=month
        )

        # Total expenses
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

        # Expenses by category (single query using annotate and values)
        expenses_by_category = expenses.values(
            category_name=F('category__name')
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('-total_amount')

        # Build response
        response_data = {
            "total_expenses": float(total_expenses),
            "expenses_by_category": [
                {
                    "category_name": item['category_name'],
                    "total_amount": float(item['total_amount'])
                }
                for item in expenses_by_category
            ]
        }

        return Response(response_data)
