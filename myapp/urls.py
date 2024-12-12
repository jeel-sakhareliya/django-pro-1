from django.urls import path
from . import views
urlpatterns = [
    path("",views.demopage),
    path("home",views.homepage),
    path("about",views.aboutpage),
    path("contact",views.contactpage),
    path("form",views.myform),
    path("myformprocess",views.myformprocess),
]