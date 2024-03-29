from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . inherit import cartData
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def Home(request):
    data = cartData(request)
    cartItems = data['cartItems']

    #products = Product.objects.all()
    context={'cartItems':cartItems}
    return render(request,"indexs.html",context)

def gallery(request):
    data = cartData(request)
    cartItems = data['cartItems']
    posts=Category.objects.all()
    context={"posts":posts,'cartItems':cartItems}
    return render(request,"gallery.html",context)

def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/index')
    return render(request,"attendance.html",context)
    
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Customer.objects.filter(phone_number=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        trainer=request.POST.get('trainer')
        reference=request.POST.get('reference')
        address=request.POST.get('address')
        query=Customer(name=FullName,email=email,gender=gender,phone_number=PhoneNumber,dob=DOB,select_membershipplan=member,select_trainer=trainer,reference=reference,address=address)
        query.save()
        messages.success(request,"Thanks For Enrollment")
        return redirect('/join')
    return render(request,"enroll.html",context)

def plans(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    return render(request,"plans.html")

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return render(request, "cart.html", {'items':items, 'order':order, 'cartItems':cartItems})

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    total = order.get_cart_total
    if request.method == "POST":
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        phone_number = request.POST['phone_number']
        payment = request.POST['payment']
        shipping_adress = CheckoutDetail.objects.create(address=address, city=city, phone_number=phone_number, state=state, zipcode=zipcode, customer=request.user.customer, total_amount=total, order=order, payment=payment)
        shipping_adress.save()
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        id = order.id  
        alert = True
        return render(request, "checkout.html", {'alert':alert, 'id':id})
    return render(request, "checkout.html", {'items':items, 'order':order, 'cartItems':cartItems})

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action:', action)
    print('productID:', productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    update_order, created = UpdateOrder.objects.get_or_create(order_id=order, desc="Your Order is Successfully Placed.")

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    update_order.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def product_view(request, myid):
    product = Product.objects.filter(id=myid).first()
    feature = Feature.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    customer = request.user.customer
    if request.method=="POST":
        content = request.POST['content']
        review = Review(customer=customer, content=content, product=product)
        review.save()
        return redirect(f"/product_view/{product.id}")
    return render(request, "product_view.html", {'product':product, 'cartItems':cartItems, 'feature':feature, 'reviews':reviews})

def search(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method == "POST":
        search = request.POST['search']
        products = Product.objects.filter(name__contains=search)
        return render(request, "search.html", {'search':search, 'products':products, 'cartItems':cartItems})
    else:
        return render(request, "search.html")


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html", {'cartItems':cartItems})


def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method=="POST":       
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        alert = True
        return render(request, 'contact.html', {'alert':alert})
    return render(request, "contact.html", {'cartItems':cartItems})

def loggedin_contact(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method=="POST":       
        name = request.user
        email = request.user.email
        phone = request.user.customer.phone_number
        desc = request.POST['desc']
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        alert = True
        return render(request, 'loggedin_contact.html', {'alert':alert})
    return render(request, "loggedin_contact.html", {'cartItems':cartItems})

def tracker(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method == "POST":
        order_id = request.POST['order_id']
        order = Order.objects.filter(id=order_id).first()
        order_items = OrderItem.objects.filter(order=order)
        update_order = UpdateOrder.objects.filter(order_id=order_id)
        print(update_order)
        return render(request, "tracker.html", {'order_items':order_items, 'update_order':update_order})
    return render(request, "tracker.html", {'cartItems':cartItems})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":   
            username = request.POST['username']
            name=request.POST['full_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            phone_number = request.POST['phone_number']
            email = request.POST['email']

            if password1 != password2:
                alert = True
                return render(request, "register.html", {'alert':alert})
            
            user = User.objects.create_user(username=username, password=password1, email=email)
            customers = Customer.objects.create(user=user, name=name, phone_number=phone_number, email=email)
            user.save()
            customers.save()

            subject = 'Registration Confirmation'
            html_message = render_to_string('registration_email.html', {'name': name})
            plain_message = strip_tags(html_message)
            from_email = 'vishi2002@gmail.com'  # Change this to your email.
            to_email = email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            


            return render(request, "login.html")
    return render(request, "register.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                alert = True
                return render(request, "login.html", {"alert":alert})
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')

def shop(request):
    data = cartData(request)
    products = None
    categories = Category.objects.all()  # Retrieve all categories
    categoryid = request.GET.get('category')  # Get the category ID from the query parameters
    cartItems = data['cartItems']
    if categoryid:
        # Retrieve products based on the selected category
        products = Product.get_all_products_by_categoryid(categoryid)
        #products = Product.objects.filter(category_id=categoryid)
    else:
        # Retrieve all products
        #products = Product.objects.all()
        return redirect('/oops')
    data = {'products': products, 'categories': categories,'cartItems':cartItems}

    return render(request, 'shop.html', data)


