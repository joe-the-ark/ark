
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/miniapp/', views.login_miniapp, name='login_miniapp'),
    path('login/public/account/', views.login_public_account, name='login_public_account'),

    path('token/', views.get_token, name='token'),

    path('order/public/account/<product_id>/', views.order_public_account, name='order_public_account'),

    path('order/miniapp/<product_id>/', views.order_miniapp, name='order_miniapp'),
    path('order/success/<product_id>/', views.order_success, name='order_success'),
    path('wechat/pay/confirm/', views.wechat_pay_confirm, name='wechat_pay_confirm'),
    path('zhifu/wechat/<order_id>/', views.zhifu, name='zhifu'),
]
