from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer

@login_required
def expense_tracker_view(request):
    return render(request, 'expenses/index.html', {'user': request.user})

@login_required
def profile_view(request):
    return render(request, 'expenses/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'expenses/settings.html', {'user': request.user})

@login_required
def expense_history(request):
    """View for expense history with pagination and search"""
    # Get all expenses for the logged-in user, ordered by date (newest first)
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        expenses = expenses.filter(
            Q(title__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )
    
    # Category filter - support multiple categories
    category_filter = request.GET.get('category', '')
    if category_filter:
        # Check if multiple categories are passed (comma-separated)
        if ',' in category_filter:
            category_ids = category_filter.split(',')
            expenses = expenses.filter(category_id__in=category_ids)
        else:
            expenses = expenses.filter(category_id=category_filter)
    
    # Expense type filter
    expense_type_filter = request.GET.get('expense_type', '')
    if expense_type_filter:
        expenses = expenses.filter(expense_type=expense_type_filter)
    
    # Date range filter
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)
    
    # Amount range filter
    amount_min = request.GET.get('amount_min', '')
    amount_max = request.GET.get('amount_max', '')
    if amount_min:
        expenses = expenses.filter(amount__gte=amount_min)
    if amount_max:
        expenses = expenses.filter(amount__lte=amount_max)
    
    # Sorting
    sort_by = request.GET.get('sort', '-date')
    if sort_by:
        expenses = expenses.order_by(sort_by)
    
    # Pagination (10 items per page)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all().order_by('name')
    
    # Get current filter values for form pre-selection
    current_sort = request.GET.get('sort', '-date')
    current_categories = request.GET.get('category', '').split(',') if request.GET.get('category') else []
    current_amount_min = request.GET.get('amount_min', '')
    current_amount_max = request.GET.get('amount_max', '')
    current_date_from = request.GET.get('date_from', '')
    current_date_to = request.GET.get('date_to', '')
    
    context = {
        'user': request.user,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_expenses': paginator.count,
        'categories': categories,
        'current_sort': current_sort,
        'current_categories': current_categories,
        'current_amount_min': current_amount_min,
        'current_amount_max': current_amount_max,
        'current_date_from': current_date_from,
        'current_date_to': current_date_to,
    }
    
    return render(request, 'expenses/history.html', context)

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
        recent_expenses = self.get_queryset()[:5]  # Limit to 5 most recent
        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        """Get last 7 days spending data for chart"""
        # Debug: Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {'error': 'User not authenticated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        from datetime import date, timedelta
        from django.db.models import Sum
        from collections import defaultdict
        
        # Get last 7 days
        today = date.today()
        dates = []
        for i in range(6, -1, -1):
            dates.append(today - timedelta(days=i))
        
        # Get expense data for each day
        daily_spending = []
        labels = []
        
        for day_date in dates:
            day_total = self.get_queryset().filter(date=day_date).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            labels.append(day_date.strftime('%a'))  # Day name like Mon, Tue, etc.
            daily_spending.append(float(day_total))
        
        return Response({
            'labels': labels,
            'data': daily_spending
        })

@login_required
def expense_tracker_view(request):
    return render(request, 'expenses/index.html', {'user': request.user})

@login_required
def profile_view(request):
    return render(request, 'expenses/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'expenses/settings.html', {'user': request.user})
