from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import DepositProducts, DepositOptions, SaveProducts, SaveOptions, JoinDeposit, JoinSave
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SaveProductsSerializer, SaveOptionsSerializer, DepositSerializer, SaveSerializer, JoinDepositSerializer, JoinSaveSerializer
import requests
import os

EXIM_KEY = os.environ.get('EXIM_KEY')
API_KEY = os.environ.get('API_KEY')

# Create your views here.
# 환율정보 가져오기
@api_view(['GET'])
def getExim(request):
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey' : EXIM_KEY,
        'data' : 'AP01',
    }
    response = requests.get(url, params=params).json()

    return JsonResponse({'response':response})



@api_view(['GET'])
def deposit_products(request):
    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(url, params=params).json()
    baseList = response.get('result').get('baseList')

    for li in baseList:
        fin_prdt_cd = li.get('fin_prdt_cd', '')

        if not DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            save_data = {
                'fin_prdt_cd': fin_prdt_cd,
                'kor_co_nm': li.get('kor_co_nm'),
                'fin_prdt_nm': li.get('fin_prdt_nm'),
                'etc_note': li.get('etc_note'),
                'join_deny': li.get('join_deny'),
                'join_member': li.get('join_member'),
                'join_way': li.get('join_way'),
                'spcl_cnd': li.get('spcl_cnd'),
                'dcls_strt_day': li.get('dcls_strt_day')
            }
            serializer = DepositProductsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            optionList = response.get('result').get('optionList')
            for option_li in optionList:
                option_fin_prdt_cd = option_li.get('fin_prdt_cd', '')
                option_save_trm = option_li.get('save_trm', '')

                if (
                    option_fin_prdt_cd == fin_prdt_cd
                    and not DepositOptions.objects.filter(
                        fin_prdt_cd=option_fin_prdt_cd, save_trm=option_save_trm
                    ).exists()
                ):
                    instance_product = get_object_or_404(
                        DepositProducts, fin_prdt_cd=option_fin_prdt_cd
                    )
                    option_save_data = {
                        'fin_prdt_cd': option_fin_prdt_cd,
                        'intr_rate_type_nm': option_li.get('intr_rate_type_nm', ''),
                        'intr_rate': option_li.get('intr_rate', -1),
                        'intr_rate2': option_li.get('intr_rate2', -1),
                        'save_trm': option_li.get('save_trm', -1),
                    }
                    option_serializer = DepositOptionsSerializer(data=option_save_data)
                    if option_serializer.is_valid():
                        option_serializer.save(product=instance_product)

    deposit_products = DepositProducts.objects.all()
    serialized_data = DepositProductsSerializer(deposit_products, many=True).data
    return Response(serialized_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def deposit_product_options(request):
    products = DepositProducts.objects.all()
    result = []

    for product in products:
        options = DepositOptions.objects.filter(product=product)
        product_data = {
            'fin_prdt_cd': product.fin_prdt_cd,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'dcls_strt_day': product.dcls_strt_day,
        }
        for save_trm in [6, 12, 24, 36]:
            matching_option = options.filter(save_trm=save_trm).first()
            intr_rate = matching_option.intr_rate if matching_option else '000'
            product_data[f'intr_rate_{save_trm}'] = intr_rate

        result.append(product_data)

    serializer = DepositSerializer(result, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_bank(request, kor_co_nm):
    products = DepositProducts.objects.filter(kor_co_nm=kor_co_nm)
    if not products:
        return Response({"message": "Products not found for this kor_co_nm"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_detail(request, fin_prdt_cd):
    detail = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
    if not detail:
        return Response({'message': 'Product not found for this fin_prdt_cd'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DepositProductsSerializer(detail)
    return Response(serializer.data)


@api_view(['GET'])
def save_products(request):
    url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(url, params=params).json()
    baseList = response.get('result').get('baseList')

    for base_li in baseList:
        fin_prdt_cd = base_li.get('fin_prdt_cd', '')

        if not SaveProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            save_data = {
                'fin_prdt_cd': fin_prdt_cd,
                'kor_co_nm': base_li.get('kor_co_nm'),
                'fin_prdt_nm': base_li.get('fin_prdt_nm'),
                'etc_note': base_li.get('etc_note'),
                'join_deny': base_li.get('join_deny'),
                'join_member': base_li.get('join_member'),
                'join_way': base_li.get('join_way'),
                'spcl_cnd': base_li.get('spcl_cnd'),
                'dcls_strt_day': base_li.get('dcls_strt_day'),
            }
            serializer = SaveProductsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            optionList = response.get('result').get('optionList')
            for option_li in optionList:
                option_fin_prdt_cd = option_li.get('fin_prdt_cd', '')
                option_save_trm = option_li.get('save_trm', '')

                if (
                    option_fin_prdt_cd == fin_prdt_cd
                    and not SaveOptions.objects.filter(
                        fin_prdt_cd=option_fin_prdt_cd, save_trm=option_save_trm
                    ).exists()
                ):
                    instance_product = get_object_or_404(
                        SaveProducts, fin_prdt_cd=option_fin_prdt_cd
                    )
                    option_save_data = {
                        'fin_prdt_cd': option_fin_prdt_cd,
                        'intr_rate_type_nm': option_li.get('intr_rate_type_nm', ''),
                        'intr_rate': option_li.get('intr_rate', -1),
                        'intr_rate2': option_li.get('intr_rate2', -1),
                        'save_trm': option_li.get('save_trm', -1),
                    }
                    option_serializer = SaveOptionsSerializer(data=option_save_data)
                    if option_serializer.is_valid():
                        option_serializer.save(product=instance_product)

    save_products = SaveProducts.objects.all()
    serialized_data = SaveProductsSerializer(save_products, many=True).data
    return Response(serialized_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def save_product_options(request):
    products = SaveProducts.objects.all()
    result = []

    for product in products:
        options = SaveOptions.objects.filter(product=product)
        product_data = {
            'fin_prdt_cd': product.fin_prdt_cd,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'dcls_strt_day': product.dcls_strt_day,
        }
        for save_trm in [6, 12, 24, 36]:
            matching_option = options.filter(save_trm=save_trm).first()
            intr_rate = matching_option.intr_rate if matching_option else '000'
            product_data[f'intr_rate_{save_trm}'] = intr_rate

        result.append(product_data)

    serializer = SaveSerializer(result, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def save_bank(request, kor_co_nm):
    products = SaveProducts.objects.filter(kor_co_nm=kor_co_nm)
    if not products:
        return Response({"message": "Products not found for this kor_co_nm"}, status=status.HTTP_404_NOT_FOUND)
    serializer = SaveProductsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def save_detail(request, fin_prdt_cd):
    detail = SaveProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
    if not detail:
        return Response({'message': 'Product not found for this fin_prdt_cd'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SaveProductsSerializer(detail)
    return Response(serializer.data)



# 상품 가입/취소
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def join_deposit(request, deposit_id):
    if request.method == 'GET':
        joins = JoinDeposit.objects.filter(user=request.user)
        serializer = JoinDepositSerializer(joins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        deposit_product_instance = get_object_or_404(DepositProducts, id=deposit_id)

        # Check if the user is already joined to the deposit product
        if JoinDeposit.objects.filter(user=request.user, product=deposit_product_instance).exists():
            return Response({'error': 'User is already joined to the deposit product'}, status=status.HTTP_400_BAD_REQUEST)

        temp_data = {'user': request.user.id, 'product': deposit_product_instance.id}

        serializer = JoinDepositSerializer(data=temp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            join_instance = JoinDeposit.objects.get(user=request.user, product_id=deposit_id)
            join_instance.delete()
            return Response({'success': 'Product unjoined successfully'}, status=status.HTTP_204_NO_CONTENT)
        except JoinDeposit.DoesNotExist:
            return Response({'error': 'JoinDeposit not found for the given deposit_id'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def join_save(request, save_id):
    if request.method == 'GET':
        joins = JoinSave.objects.filter(user=request.user)
        serializer = JoinSaveSerializer(joins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        save_product_instance = get_object_or_404(SaveProducts, id=save_id)

        # Check if the user is already joined to the save product
        if JoinSave.objects.filter(user=request.user, product=save_product_instance).exists():
            return Response({'error': 'User is already joined to the save product'}, status=status.HTTP_400_BAD_REQUEST)

        temp_data = {'user': request.user.id, 'product': save_product_instance.id}

        serializer = JoinSaveSerializer(data=temp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        try:
            join_instance = JoinSave.objects.get(user=request.user, product_id=save_id)
            join_instance.delete()
            return Response({'success': 'Product unjoined successfully'}, status=status.HTTP_204_NO_CONTENT)
        except JoinSave.DoesNotExist:
            return Response({'error': 'JoinSave not found for the given save_id'}, status=status.HTTP_404_NOT_FOUND)
