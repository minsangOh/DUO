from django.contrib import admin
from .models import User, Family, IncomeExpense

# Register your models here.
admin.site.register(User)
admin.site.register(Family)
admin.site.register(IncomeExpense)