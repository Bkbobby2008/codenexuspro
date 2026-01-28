from django.shortcuts import render
from .models import * 
from .models import views
from . models import CustomerRegistrationForm



# customer registration form

class CustomerRegistrationView(views):
    def get(request,self):
        form = CustomerRegistrationView()
        return render(request,'app/customerregistration.html',locals())