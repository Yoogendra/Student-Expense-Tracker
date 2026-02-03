from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'expense_type', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        
        # Total expenses
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # This month's expenses
        current_month = timezone.now().replace(day=1)
        monthly_total = queryset.filter(date__gte=current_month).aggregate(total=Sum('amount'))['total'] or 0
        
        # By category
        category_breakdown = queryset.values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        return Response({
            'total_expenses': total_amount,
            'monthly_total': monthly_total,
            'category_breakdown': list(category_breakdown),
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_expenses = self.get_queryset()[:10]
        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)

@login_required
def expense_tracker_view(request):
    return render(request, 'expenses/index.html', {'user': request.user})
