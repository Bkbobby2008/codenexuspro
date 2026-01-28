from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import  redirect, get_object_or_404,render,redirect
from django.views import View  # Corrected import for class-based views
from . models import Product,Cart
from .forms import CustomerRegistrationForm
from django.contrib import messages
from .models import Customer,Payment,OrderPlaced
from .forms import CustomerProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseBadRequest




# Create your views here.
def home(request):
    return render(request, 'app/home.html')

# About page
def about(request):
    return render(request, 'app/about.html')

# contact page
def contact(request):
    return render(request, 'app/contact.html')


# Create your login page
class LoginView(View):
    def get(self, request):
        return render(request, 'app/login.html')
    def post(self, request):
        return redirect('home') 
    
# category view
class CategoryView(View):  # Changed to inherit from View
    def get(self, request ,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')                                                          
        return render(request, "app/category.html",locals())

# category title 
class CategoryTitle(View):  # Changed to inherit from View
    def post(self, request ,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')                                                          
        return render(request, "app/category.html",locals())

# product detail
class ProductDetail(View):  # Changed to inherit from View
    def get(self, request,pk):
        product = Product.objects.get(pk = pk)
        return render(request, "app/productdetail.html",locals())
    

# logout_view
def logoutView(request):
    logout(request)
    return redirect('login') 

# Customer Registration View
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation! User Register Successful')
        else:
            messages.error(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

# Customer(5)

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # Associate customer with user
            customer.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, 'app/profile.html', {'form': form})
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})  # Changed template to 'address.html'



class updateAddress(View):
    def get(self, request, pk):
        add = get_object_or_404(Customer, pk=pk, user=request.user)  # Ensure user can only update their own address
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', {'form': form, 'add': add})

    def post(self, request, pk):
        add = get_object_or_404(Customer, pk=pk, user=request.user)  # Ensure correct instance
        form = CustomerProfileForm(request.POST, instance=add)  # Update instead of creating new instance
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect("address")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, 'app/updateAddress.html', {'form': form, 'add': add})  # Re-render form with errors
    
# add to card
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart= Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount + value
    totalamount = amount + 40


    
    return render(request,'app/addtocart.html',locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = sum(p.quantity * p.product.discount_price for p in cart_items)
        totalamount = famount 
        razoramount = int(totalamount * 100)
        
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid12"}
        
        payment_response = client.order.create(data=data)
        #{'amount': 15000, 'amount_due': 15000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1742491593, 'currency': 'INR', 'entity': 'order', 'id': 'order_Q97ut3IM5aCnMO', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid12', 'status': 'created'}
        order_id = payment_response.get('id')
        order_status = payment_response.get('status')
        
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
            return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalamount': totalamount, 'order_id': order_id})
        else:
            return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalamount': totalamount, 'order_id': order_id})

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    #print("payment_done : oid = ",order_id,"pid = ",payment_id,"cid = ",cust_id)
    user = request.user
    customer = Customer.objects.get(id =cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user ,customer = customer, product = c.product, quantity= c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

# Plus Cart
def plus_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        cart_item = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()

            # Recalculate total amount
            cart = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discount_price for p in cart)
            totalamount = amount + 40

            return JsonResponse({'quantity': cart_item.quantity, 'amount': amount, 'totalamount': totalamount})

        return JsonResponse({'error': 'Product not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Minus Cart
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  # Fixed Syntax
        cart_item = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            # Recalculate total amount
            cart = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discount_price for p in cart)
            totalamount = amount + 40

            return JsonResponse({'quantity': cart_item.quantity if cart_item else 0, 'amount': amount, 'totalamount': totalamount})

        return JsonResponse({'error': 'Product not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Remove Cart
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  # Fixed Syntax
        cart_item = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.delete()

            # Recalculate total amount
            cart = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discount_price for p in cart)
            totalamount = amount + 40

            return JsonResponse({'amount': amount, 'totalamount': totalamount})

        return JsonResponse({'error': 'Product not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def payment(request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # ✅ Subtotal Calculation (Only Cart Items)
        subtotal = sum(item.quantity * item.product.discount_price for item in cart_items)
        delivery_charge = 40  # ₹40 Fixed Delivery Charge
        totalamount = subtotal + delivery_charge  # ✅ Correct Total Calculation

        # Razorpay Order Create
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        order_data = {"amount": int(totalamount * 100), "currency": "INR", "receipt": f"order_{user.id}"}
        payment_response = client.order.create(data=order_data)

        order_id = payment_response.get('id')

        # Save Payment Data
        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=payment_response.get('status')
        )
        payment.save()

        return render(request, 'app/payment.html', {
            'subtotal': subtotal,  # ✅ Send Subtotal
            'delivery_charge': delivery_charge,  # ✅ Send Delivery Charge
            'totalamount': totalamount,  # ✅ Send Correct Total Amount
            'razorpay_amount': int(totalamount * 100),  # Razorpay Needs Amount in Paise
            'razorpay_key': settings.RAZOR_KEY_ID,
            'order_id': order_id
        })


def payment_success(request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # ✅ Subtotal Calculation
        subtotal = sum(item.quantity * item.product.discount_price for item in cart_items)
        delivery_charge = 40  # ₹40 Fixed Delivery Charge
        totalamount = subtotal + delivery_charge  # ✅ Correct Total Calculation

        # ✅ Payment Details from Query Params
        payment_id = request.GET.get('payment_id', 'N/A')
        order_id = request.GET.get('order_id', 'N/A')

        context = {
            'user': user,
            'cart_items': cart_items,  # ✅ Show Ordered Items
            'subtotal': subtotal,  
            'delivery_charge': delivery_charge,  
            'totalamount': totalamount,  
            'payment_id': payment_id,
            'order_id': order_id,
        }
        return render(request, 'app/success.html', context)



client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

import hmac
import hashlib
import json

RAZOR_KEY_SECRET = "n16wn6yLzy6kWegRBwJTs0So"

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        # Step 1: Verify signature
        generated_signature = hmac.new(
            bytes(settings.RAZOR_KEY_SECRET, 'utf-8'),
            bytes(razorpay_order_id + "|" + razorpay_payment_id, 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            # ✅ Payment is secure and verified
            return JsonResponse({'success': True})
        else:
            # ❌ Signature didn't match
            return JsonResponse({'success': False, 'error': 'Invalid signature'})