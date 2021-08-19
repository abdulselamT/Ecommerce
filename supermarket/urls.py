from django.urls import path
from . import views
urlpatterns = [
	path('', views.homepage, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('register/', views.registercustomer, name="register"),
	path('registerproduct/', views.registerproduct, name="registerproduct"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('addtocart/<str:pk>/', views.addtocart, name="addtocart"),
	]