from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="index"),
    # redirect any link of the form 127.0.0.1:8000/<string> to redirectFunc in views
    path('<str:short>',views.redirectFunc,name="redirection"),  

    # API views of all the URLS present in the database 
    # can be accessed at 127.0.0.1:8000/allurls/ 
    path('allurls/',views.URLAPI.as_view(),name='min'),

    

]
