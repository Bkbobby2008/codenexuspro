from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views
from .forms import MyPasswordResetForm, MyPasswordChangeForm,MySetPasswordForm
from .views import home, CategoryView, CategoryTitle, ProductDetail, updateAddress

urlpatterns = [
    # Home and general pages
    path('', home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # add-to-card
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    # path('checkout/',views.show_cart, name='checkout'),
    path('checkout/',views.checkout.as_view(), name='checkout'),

    # plus cart/minus
    path('pluscart/', views.plus_cart, name="pluscart"),
    path('minuscart/', views.minus_cart, name="minuscart"),
    path('removecart/', views.remove_cart, name="removecart"),
    
    # Category and product pages
    path('category/<slug:val>/', CategoryView.as_view(), name='category'),
    path('category-title/<val>/', CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', ProductDetail.as_view(), name='productdetail'),

    # User profile and address management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('update-address/<int:pk>/', updateAddress.as_view(), name='updateAddress'),

    # Customer registration and authentication
    path('register/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logoutView, name='logout'),
 

    # Password reset and change
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm
    ), name='password-reset'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,
        success_url='/password-change-done'), name='passwordchange'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/passwordChangedone.html'
    ), name='passwordChangedone'),

    # password reset 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html' 
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm
    ),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complte.html' 
    ), name='password_reset_complte'),

    # payment-card
    path('payment/', views.payment, name="payment"),    
    path('paymentdone/', views.payment_done, name="paymentdone"),    
    path('payment_success/', views.payment_success, name='payment_success'),  # Success Page

path('verify_payment/', views.verify_payment, name='verify_payment'),


]

# Static and media file configuration (for development only)
if settings.DEBUG or True: # Render par True ki tarah treat karein agar images chahiye
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

