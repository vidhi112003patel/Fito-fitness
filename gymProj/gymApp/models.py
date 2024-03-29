from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    gender=models.CharField(max_length=25,default='m/f')
    dob = models.CharField(max_length=50, default='YYYY-MM-DD')
    select_membershipplan=models.CharField(max_length=200,default='plan')
    select_trainer=models.CharField(max_length=55,default='trainer')
    reference=models.CharField(max_length=55,default='reference')
    address = models.TextField(default='123 Main St, City, Country')  
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.user)



class Category(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='gallery')
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="", default="")

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter (id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter (category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.product) + " Feature: " + self.feature

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.customer) +  " Review: " + self.content

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(default=now)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class UpdateOrder(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    desc = models.CharField(max_length=500)
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.order_id)

class CheckoutDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True,null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    payment = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.address

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name=models.CharField(max_length=55)
    gender=models.CharField(max_length=25)
    phone=models.CharField(max_length=25)
    salary=models.IntegerField(max_length=25)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name
    
class MembershipPlan(models.Model):
    plan=models.CharField(max_length=185)
    price=models.IntegerField(max_length=55)

    def __int__(self):
        return self.id


class Attendance(models.Model):
    Selectdate=models.DateTimeField(auto_now_add=True)
    phonenumber=models.CharField(max_length=15)
    Login=models.CharField(max_length=200)
    Logout=models.CharField(max_length=200)
    SelectWorkout=models.CharField(max_length=200)
    TrainedBy=models.CharField(max_length=200)

    def __int__(self):
        return self.id

