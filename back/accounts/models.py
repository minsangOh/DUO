from django.db import models
from django.contrib.auth.models import AbstractUser
from apis.models import DepositProducts, SaveProducts

# Create your models here.


# 유저 모델
class User(AbstractUser):
    JOB_CHOICES = [
        ('management', '경영/사무/금융/보험직'),
        ('engineering', '연구직 및 공학 기술직'),
        ('education', '교육/법률/사회복지/경찰/소방직 및 군인'),
        ('health', '보건/의료직'),
        ('arts', '예술/디자인/방송/스포츠직'),
        ('service', '미용/여행/숙박/음식/경비/청소직'),
        ('sales', '영업/판매/운전/운송직'),
        ('construction', '건설/채굴직'),
        ('production', '설치/정비/생산직'),
        ('agriculture', '농림어업직'),
    ]

    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=5)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    age = models.IntegerField(null=True)
    money = models.IntegerField(null=True)  # 현재 자산
    salary = models.IntegerField(null=True)  # 월급
    job = models.CharField(max_length=100, blank=True, null=True,  choices=JOB_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    financial_products_deposit = models.ManyToManyField(DepositProducts, blank=True)
    financial_products_save = models.ManyToManyField(SaveProducts, blank=True)
    # superuser fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'


# 가족 모델
class Family(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marriage_date = models.DateField(blank=True, null=True)
    children_plan = models.BooleanField(default=False)


# 소득 지출 모델
class IncomeExpense(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    monthly_fixed_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    monthly_savings = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
