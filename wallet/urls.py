# urls.py

from django.urls import path
from .views import get_wallet, recharge_wallet, record_transaction

urlpatterns = [
    path('wallet/', get_wallet, name='get_wallet'),
    path('wallet/recharge/', recharge_wallet, name='recharge_wallet'),
    path('wallet/record/', record_transaction, name='record_transaction'),
]
