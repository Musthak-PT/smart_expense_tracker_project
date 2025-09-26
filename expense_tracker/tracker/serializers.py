# tracker/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Expense

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        # Use create_user to hash password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)              # nested user in responses
    category = CategorySerializer(read_only=True)      # nested category in responses
    category_id = serializers.PrimaryKeyRelatedField(  # write-only field for creating/updating
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=True
    )

    class Meta:
        model = Expense
        fields = [
            'id',
            'user', 'category', 'category_id',
            'amount', 'description', 'date'
        ]
        read_only_fields = ('id', 'user', 'category')  # category included as nested in read responses
