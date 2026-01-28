from django.contrib import admin
from . models import Product,Customer,Cart,Payment,OrderPlaced

#Register your model here 
 
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'selling_price', 'discount_price', 'category','product_image']  # Fields to display in the list view


# profile(1)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'location', 'city', 'state', 'zipcode']

# cart
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','products','quantity','ordered_date','status','payments']