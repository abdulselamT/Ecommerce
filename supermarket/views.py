from django.shortcuts import render,redirect
from.forms import *
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def homepage(request):
	products=Product.objects.all()
	context={'products':products}
	return render(request,'supermarket/store.html',context)
def cart(request):
	context={}
	return render(request,'supermarket/cart.html',context)

def checkout(request):
	context={}
	return render(request,'supermarket/checkout.html',context)
@unauthenticated_user
def registercustomer(request):
	form=CreateUserForm()
	customerform=CustomerForm()
	print("working1")
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		customerform=CustomerForm(request.POST,request.FILES)
		print("working2")
		if form.is_valid() and customerform.is_valid():
			group=Group.objects.get(name='customer')
			user=form.save()
			user.groups.add(group)
			customer=customerform.save(commit=False)
			print("working3")
			customer.user=user
			customer.save()
			y=Product.objects.all()
			for k in y:
				Order.objects.create(customer=Customer.objects.last(),product=k)
				print("order is running")
			return redirect('store')
	context={"form":form,"customerform":customerform}
	return render(request,'supermarket/register.html',context)

def registerproduct(request):
	form = ProductForm()
	if request.method=="POST":
		form=ProductForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			y=Customer.objects.all()
			for k in y:
				Order.objects.create(product=Product.objects.last(),customer=k)
				print("order is running")
			return redirect('store')
	context={'form':form}
	return render(request,'supermarket/register.html',context)
@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'supermarket/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def addtocart(requiest,pk):
	x=Product.objects.get(id=pk)
	y=Order.objects.filter(product=x).filter(customer=requiest.user.customer)
	print(y)
	print(y.added)
	if y.added:
		y.added=False
		y.save()
	else:
		y.added=True
		y.save()
	return redirect('store')