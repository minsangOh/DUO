from django.urls import path, include
from . import views

urlpatterns = [
    path('exim/', views.getExim),

    # 예금상품 DepositProducts (get: 저장(옵션 및 상품) 및 상품 조회)
    path('deposit-products/', views.deposit_products),
    # 정기예금 상세
    path('deposit-detail/<str:fin_prdt_cd>/', views.deposit_detail),
    # 예금상품의 옵션 리스트
    path('deposit-product-options/', views.deposit_product_options),
    # 특정 회사의 예금상품 리스트
    path('deposit-bank/<str:kor_co_nm>/', views.deposit_bank),

    # 적금상품 SaveProducts (get: 저장(옵션 및 상품) 및 상품 조회)
    path('save-products/', views.save_products),
    # 정기적금 상세
    path('save-detail/<str:fin_prdt_cd>/', views.save_detail),
    # 특정 적금상품의 옵션 리스트
    path('save-product-options/', views.save_product_options),
    # 특정 회사의 적금상품 리스트
    path('save-bank/<str:kor_co_nm>/', views.save_bank),

    # 상품 가입 및 취소
    path('joindeposit/<str:deposit_id>/', views.join_deposit),
    path('joinsave/<str:save_id>/', views.join_save),

]
