from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # This is my URL pattern for the index page
    path('', views.index, name='index'),

    # This is my URL pattern for the login page
    path('login/', auth_views.LoginView.as_view(template_name='happy_hoe/login.html'), name='login'),

    # This is my URL pattern for the dashboard page
    path('dashboard/', views.dashboard, name='dashboard'),

    # This is my URL pattern for deleting a product by its ID
    path('delete/<int:product_id>/', views.delete_detail, name='delete_detail'),

    # This is my URL pattern for viewing product details by its ID
    path('home/<int:product_id>/', views.product_detail, name='product_detail'),

    # This is my URL pattern for issuing an item by its ID
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),

    # This is my URL pattern for viewing the receipt page
    path('receipt/', views.receipt, name='receipt'),

    # This is my URL pattern for viewing details of a specific receipt by its ID
    path('all_receipts/<int:receipt_id>/', views.all_receipts, name='all_receipts'),

    # This is my URL pattern for viewing all sales
    path('allsales/', views.allsales, name='allsales'),

    # This is my URL pattern for logging out
    path('logout/', views.custom_logout, name='logout'),

    # This is my URL pattern for adding stock by its ID
    path('add_stock/<str:pk>/', views.add_stock, name='add_stock'),
]
