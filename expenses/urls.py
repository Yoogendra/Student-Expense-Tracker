from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, expense_tracker_view, profile_view, settings_view, expense_history
from . import views_auth

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', expense_tracker_view, name='expense_tracker'),
    path('login/', views_auth.login_view, name='login'),
    path('register/', views_auth.register_view, name='register'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('api/auth/login/', views_auth.api_login, name='api_login'),
    path('api/auth/register/', views_auth.api_register, name='api_register'),
    path('api/expenses/chart-data/', ExpenseViewSet.as_view({'get': 'chart_data'}), name='chart_data'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('history/', expense_history, name='expense_history'),
]
