from django.contrib import admin
from .models import DepositProducts, DepositOptions, JoinDeposit, SaveProducts, SaveOptions, JoinSave

# Register your models here.
admin.site.register(DepositProducts)
admin.site.register(DepositOptions)
admin.site.register(JoinDeposit)
admin.site.register(SaveProducts)
admin.site.register(SaveOptions)
admin.site.register(JoinSave)