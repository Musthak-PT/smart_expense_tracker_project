from django.contrib import admin
from .models import Category, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')          # Columns shown in list view
    search_fields = ('name',)              # Search by name
    ordering = ('name',)                   # Default ordering in admin


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'amount', 'date', 'description')
    list_filter = ('category', 'date')     # Sidebar filters
    search_fields = ('user__username', 'category__name', 'description')  # Search across related fields
    date_hierarchy = 'date'                # Adds a date drill-down navigation
    ordering = ('-date',)                  # Default ordering
    readonly_fields = ('id',)              # ID is read-only in admin
