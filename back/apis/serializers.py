from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SaveProducts, SaveOptions, JoinDeposit, JoinSave

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='DepositOptions.product')
    class Meta:
        model = DepositOptions
        fields = '__all__'

class DepositSerializer(serializers.Serializer):
    fin_prdt_cd = serializers.CharField()
    kor_co_nm = serializers.CharField()
    fin_prdt_nm = serializers.CharField()
    dcls_strt_day= serializers.CharField()
    intr_rate_6 = serializers.FloatField(required=False)
    intr_rate_12 = serializers.FloatField(required=False)
    intr_rate_24 = serializers.FloatField(required=False)
    intr_rate_36 = serializers.FloatField(required=False)

class SaveProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveProducts
        fields = '__all__'

class SaveOptionsSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='SaveOptions.product')
    class Meta:
        model = SaveOptions
        fields = '__all__'

class SaveSerializer(serializers.Serializer):
    fin_prdt_cd = serializers.CharField()
    kor_co_nm = serializers.CharField()
    fin_prdt_nm = serializers.CharField()
    dcls_strt_day= serializers.CharField()
    intr_rate_6 = serializers.FloatField(required=False)
    intr_rate_12 = serializers.FloatField(required=False)
    intr_rate_24 = serializers.FloatField(required=False)
    intr_rate_36 = serializers.FloatField(required=False)

class JoinSaveSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=SaveProducts.objects.all())
    class Meta:
        model = JoinSave
        fields = '__all__'

class JoinDepositSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=DepositProducts.objects.all())
    class Meta:
        model = JoinDeposit
        fields = '__all__'
