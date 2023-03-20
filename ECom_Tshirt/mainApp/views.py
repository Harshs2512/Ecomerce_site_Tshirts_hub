from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import RegistrationForm, CustomerProfileForm, CheckoutForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        # request.session['customer'] = email
        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        # if not user_obj[0].profile.is_email_verified:
        #     print(user_obj[0])
        #     messages.warning(request, 'Your account is not verified.')
        #     return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid Username or Password')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'register.html')


def addcart(req):
    usr = req.user
    product_id = req.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart_save = cart(user=usr, product=product)
    cart_save.save()
    return redirect("/showcart")


def show_cart(req):
    if req.user.is_authenticated:
        usr = req.user
        crt = cart.objects.filter(user=usr)
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == usr]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(req, 'cart.html', {'carts': crt, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(req, 'emtycart.html')


def plus_cart(req):
    if req.method == 'GET':
        prod_id = req.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=req.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == req.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(req):
    if req.method == 'GET':
        prod_id = req.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=req.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == req.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(req):
    if req.method == 'GET':
        prod_id = req.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=req.user))
        # c.quantity -= 1
        c.delete()
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == req.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def checkout(req):
    usr = req.user
    userdetail = User.objects.filter(email=usr)
    address = Customer.objects.filter(user=usr)
    cart_item = cart.objects.filter(user=usr)
    dis = [d for d in Customer.objects.all()]
    for d in dis:
        display = d.locality
        if display:
            display_res = 'none'
            print(display_res)
        else:
            display_res = 'n'
    total = [p for p in cart.objects.all() if p.user == req.user]
    amount = 0
    form = CheckoutForm()
    for p in total:
        tempamount = (p.quantity * p.product.selling_price)
        amount += tempamount
        subtotal = amount+80
    return render(req, 'checkout.html', {'form': form, 'address': address, 'cart_item': cart_item, 'amount': amount, 'subtotal': subtotal, 'userdetail': userdetail, 'display': display_res})


def payment_done(req):
    usr = req.user
    custid = req.GET.get('custid')
    customer_data = Customer.objects.get(id=custid)
    cart_item = cart.objects.filter(user=usr)
    for c in cart_item:
        OrderPlaced(user=usr, customer=customer_data,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('/oders')
    # return HttpResponse(custid)


def oders(req):
    od = OrderPlaced.objects.filter(user=req.user)
    a = Product.objects.all()
    print(a)
    return render(req, 'oders.html', {'cus_oder': od})


# -------------------------------------------------------?


class ProductView(View):
    def get(self, req):
        usr = req.user
        T_Shirt = Product.objects.filter(category='T')
        count_Tshirt = Product.objects.filter(category='T').count()
        Hoodies = Product.objects.filter(category='H')
        count_hoodies = Product.objects.filter(category='H').count()
        Coding_Tshirt = Product.objects.filter(category='CT')
        count_Coding_Tshirt = Product.objects.filter(category='CT').count()
        Anime_TShirt = Product.objects.filter(category='AT')
        count_Anime_TShirt = Product.objects.filter(category='AT').count()
        count_cart_product = cart.objects.filter(user=usr).count()
        return render(req, 'index.html', {'T_Shirt': T_Shirt,
                                          'Hoodies': Hoodies,
                                          'Coding_Tshirt': Coding_Tshirt,
                                          'Anime_TShirt': Anime_TShirt,
                                          'count_Tshirt': count_Tshirt,
                                          'count_hoodies': count_hoodies,
                                          'count_Anime_TShirt': count_Anime_TShirt,
                                          'count_Coding_Tshirt': count_Coding_Tshirt,
                                          'count_cart_product': count_cart_product})


class ProductDetailView(View):
    def get(self, req, pk):
        print(pk)
        products = Product.objects.get(pk=pk)
        return render(req, 'detail.html', {'products': products})


class ShopView(View):
    def get(self, req):
        products = Product.objects.filter()
        return render(req, 'shop.html', {'products': products})


class ShopCetegoryView(View):
    def get(self, req, item):
        products = Product.objects.filter(category=item)
        print(products)
        return render(req, 'shop.html', {'products': products})


class ProfileView(View):
    def get(self, req):
        usr = req.user
        cus = req.user.id
        # print(cus)
        form = CustomerProfileForm()
        userdetail = User.objects.filter(username=usr)
        custoer_detail = Customer.objects.filter(user_id=cus)
        # print(custoer_detail)
        return render(req, 'profile.html', {'form': form, 'userdetail': userdetail, 'custoer_detail': custoer_detail})

    def post(self, req):
        form = CustomerProfileForm(req.POST)
        if form.is_valid():
            usr = req.user
            print(usr)
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(req, "Congratulation")
        # customer_detail = Customer.objects.filter(id=)
        return redirect('/')
