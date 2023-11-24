from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter
from .models import User
from apis.models import DepositProducts, SaveProducts
from dj_rest_auth.registration.serializers import RegisterSerializer
from apis.models import JoinDeposit, JoinSave


# 회원가입 시 사용할 Serializer 재정의.
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=5)
    last_name = serializers.CharField(max_length=20)
    nickname = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    job = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    location = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    financial_products_deposit = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DepositProducts.objects.all(), required=False)
    financial_products_save = serializers.PrimaryKeyRelatedField(
        many=True, queryset=SaveProducts.objects.all(), required=False)

    # 필드를 재정의 하면서 추가된 필드 추가
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', ''),
            'money': self.validated_data.get('money', ''),
            'salary': self.validated_data.get('salary', ''),
            'job': self.validated_data.get('job', ''),
            'location': self.validated_data.get('location', ''),
            'financial_products_deposit': self.validated_data.get('financial_products_deposit', ''),
            'financial_products_save': self.validated_data.get('financial_products_save', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        # 새로운 필드를 사용자 모델에 저장
        user.nickname = self.cleaned_data.get('nickname')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.age = self.cleaned_data.get('age')
        user.money = self.cleaned_data.get('money')
        user.salary = self.cleaned_data.get('salary')
        user.job = self.cleaned_data.get('job')
        user.location = self.cleaned_data.get('location')
        user.financial_products_deposit.set(
            self.cleaned_data.get('financial_products_deposit', []))
        user.financial_products_save.set(
            self.cleaned_data.get('financial_products_save', []))
        user.save()

        self.custom_signup(request, user)
        return user


# 유저 모델
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=False, allow_blank=True, max_length=get_username_max_length())
    password = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    first_name = serializers.CharField(
        max_length=5, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=20, required=False, allow_blank=True)
    nickname = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    job = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    joined_deposits = serializers.SerializerMethodField()
    joined_savings = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def get_joined_deposits(self, user):
        # `JoinDeposit` 모델에서 사용자와 연결된 예금 상품 목록을 반환하는 로직
        deposits = JoinDeposit.objects.filter(user=user)
        return [deposit.product.fin_prdt_nm for deposit in deposits]
    
    def get_joined_savings(self, user):
        savings = JoinSave.objects.filter(user=user)
        return [saving.product.fin_prdt_nm for saving in savings]
    
    class Meta:
        model = User
        fields = '__all__'  # 모든 필드를 포함합니다.
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
