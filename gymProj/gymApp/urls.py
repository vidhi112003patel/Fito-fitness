from django.conf import settings
from django.urls import path
from gymApp import views
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Home,name="Home"),
   #path("", views.index, name="index"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("product_view/<int:myid>/", views.product_view, name="product_view"),
    path("search/", views.search, name="search"),
    path("tracker/", views.tracker, name="tracker"),
    path("contact/", views.contact, name="contact"),
    path("loggedin_contact/", views.loggedin_contact, name="loggedin_contact"),

    path("register/", views.register, name="register"),
    path("change_password/", views.change_password, name="change_password"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    path('join/',views.enroll,name="enroll"),
    path('profile/',views.profile,name="profile"),
    path('gallery/',views.gallery,name="shopnow"),
    path('attendance/',views.attendance,name="attendance"),
    path('plans/',views.plans,name="membershipplans"),
    path('shop/', views.shop , name='shop'),
    path('shop/profile/', views.profile, name="profile"),
    path('shop/join/', views.enroll, name="enroll"),
    path('shop/plans/', views.plans, name="membershipplans")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
