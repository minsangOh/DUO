from django.urls import path, include
from accounts.views import CustomUserDetailsView
# dj_rest_auth.urls 커스터마이징을 위한 import
# dj-rest-auth를 사용하지 않아 패키지가 업데이트 될 경우 업데이트 내용에 대하여 유지보수 필요
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView,)
from . import views

urlpatterns = [
    # URLs that do not require a session or valid token
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('delete/', views.delete_account, name='delete_account'),

    # URLs that require a user to be logged in with a valid session / token.
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    # path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('myinfo/', CustomUserDetailsView.as_view(), name='my_details'),
    path('myinfo/<int:user_pk>/', views.user_detail, name='modified'),
    path('user/<int:user_pk>/', views.user_detail, name='user_detail'),
    path('recommend_products_deposit/<int:user_id>/', views.product_recommendations_deposit, name='product_recommendations_deposit'),
    path('recommend_products_save/<int:user_id>/', views.savings_recommendations_save, name='savings_recommendations_save'),
    path('graph/<int:user_id>/', views.financial_graph, name='graph'),
    
    path('top3deposits/', views.top_deposits_by_location_and_job, name='top3deposits'),
    path('top3saves/', views.top_saves_by_location_and_job, name='top3saves'),
]   

if api_settings.USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns = [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
