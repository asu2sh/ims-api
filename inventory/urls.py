from django.urls import path
from .views import ItemView, RegisterView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('items/', ItemView.as_view(), name='item_list'),
    path('items/<int:item_id>', ItemView.as_view(), name='item_detail'),

    path('auth/register/', RegisterView.as_view(), name='register_user'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
