# Standard library imports
import base64
import os
from io import BytesIO

# Django related imports
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count


# Django REST framework imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dj_rest_auth.views import UserDetailsView

# Matplotlib and Sklearn related imports
import matplotlib
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt


# Local application/model imports
from .models import User
from .serializers import UserSerializer
from apis.models import DepositOptions, SaveOptions, DepositProducts, SaveProducts, JoinSave, JoinDeposit

# Create your views here.


class CustomUserDetailsView(UserDetailsView):
    serializer_class = UserSerializer

# 유저 프로필 조회 및 수정


@api_view(['GET', 'PUT'])
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        # print(serializer.data)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = request.data
        for field in data:
            setattr(user, field, data[field])
        user.save()
        return Response(status=status.HTTP_200_OK)

# 계정 삭제


@api_view(['Delete'])
def delete_account(request):
    if request.user.is_authenticated:
        plain_password = request.data.get('password')
        if check_password(plain_password, request.user.password):
            request.user.delete()   # 반드시 먼저 계정 삭제부터.
            auth_logout(request)    # 로그아웃 먼저 하면 뭘 삭제해야할지 알 수 없어짐.
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "비밀번호를 확인하세요"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)






# 개인별 예적금 가입 상품 금리 비교 이미지 출력
def financial_graph(request, user_id):
    # 한글 문자를 지원하는 폰트 설정
    font_path = os.path.join(
        settings.BASE_DIR, 'accounts/static/fonts/NanumBarunGothic.ttf')
    font_prop = font_manager.FontProperties(fname=font_path)
    # 폰트 설정을 전역으로 적용
    plt.rc('font', family=font_prop.get_name())
    plt.rc('axes', unicode_minus=False)  # 마이너스 부호가 깨지지 않도록 설장
    matplotlib.use('Agg')
    # 사용자 객체 가져오기
    user = User.objects.get(id=user_id)
    # 고려할 기간
    terms = [6, 12, 24, 36]

    # 기간별 적금 금리 데이터
    save_rates_data = {term: [] for term in terms}
    # 각 적금 상품별로 기간에 따른 금리 수집
    save_product_names = []  # 상품 이름을 저장할 리스트 초기화
    for join_save in JoinSave.objects.filter(user=user):  # JoinSave 모델 사용
        product = join_save.product
        save_product_names.append(product.fin_prdt_nm)  # 리스트에 상품 이름 추가
        options = SaveOptions.objects.filter(
            product=product, save_trm__in=terms)
        product_rates = {term: 0 for term in terms}  # 해당 상품의 기간별 금리 초기화

        for option in options:
            product_rates[option.save_trm] = option.intr_rate  # 해당 기간의 금리 저장

        for term in terms:
            save_rates_data[term].append(product_rates[term])  # 각 기간에 대한 금리 추가

    # 그래프 생성
    if any(save_rates_data.values()):
        plt.figure(figsize=(10, 6))
        width = 0.2
        colors = ['#a9c9ff', '#94d2bd', '#f4d35e', '#ef9f9f']

        for idx, term in enumerate(terms):
            plt.bar([x + width*idx for x in range(len(save_product_names))],
                    save_rates_data[term], width=width, label=f'{term} Months', color=colors[idx % len(colors)],)

        plt.xlabel('가입한 정기적금 상품', fontproperties=font_prop)
        plt.ylabel('저축 금리', fontproperties=font_prop)
        plt.title('정기적금 상품별 기간에 따른 저축 금리', fontproperties=font_prop)
        plt.xticks([r + width*(len(terms)-1)/2 for r in range(len(save_product_names))],
                    save_product_names, fontproperties=font_prop, rotation=45, ha='right')
        plt.legend(loc='upper right', fontsize='small', ncol=5)
        # plt.tight_layout()  # 그래프의 레이아웃을 개선
        plt.subplots_adjust(bottom=0.4)  # 아래쪽 여백을 충분히 확보


        # 그래프를 이미지로 변환
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        save_image_png = buffer.getvalue()
        buffer.close()

        # base64 인코딩
        save_graphic = base64.b64encode(save_image_png)
        save_graphic = save_graphic.decode('utf-8')
    else:
        save_graphic = None
    ############################################################################
    # 기간별 예금 금리 데이터
    deposit_rates_data = {term: [] for term in terms}
    # 각 예금 상품별로 기간에 따른 금리 수집
    deposit_product_names = []  # 상품 이름을 저장할 리스트 초기화
    # JoinDeposit 모델 사용
    for join_deposit in JoinDeposit.objects.filter(user=user):
        product = join_deposit.product
        deposit_product_names.append(product.fin_prdt_nm)  # 리스트에 상품 이름 추가
        options = DepositOptions.objects.filter(
            product=product, save_trm__in=terms)
        product_rates = {term: 0 for term in terms}  # 해당 상품의 기간별 금리 초기화

        for option in options:
            # 해당 기간의 금리 저장
            product_rates[option.save_trm] = option.intr_rate

        for term in terms:
            deposit_rates_data[term].append(
                product_rates[term])  # 각 기간에 대한 금리 추가

    

    # 그래프 생성
    if any(deposit_rates_data.values()):
        plt.figure(figsize=(10, 6))
        width = 0.2
        colors = ['#a9c9ff', '#94d2bd', '#f4d35e', '#ef9f9f']

        for idx, term in enumerate(terms):
            plt.bar([x + width*idx for x in range(len(deposit_product_names))],
                    deposit_rates_data[term], width=width, label=f'{term} Months', color=colors[idx % len(colors)],)

        plt.xlabel('가입한 정기예금 상품', fontproperties=font_prop)
        plt.ylabel('저축 금리', fontproperties=font_prop)
        plt.title('정기예금 상품별 기간에 따른 저축 금리', fontproperties=font_prop)
        plt.xticks([r + width*(len(terms)-1)/2 for r in range(len(deposit_product_names))],
                    deposit_product_names, fontproperties=font_prop, rotation=45, ha='right')
        plt.legend(loc='upper right', fontsize='small', ncol=5)
        # plt.tight_layout()  # 그래프의 레이아웃을 개선
        plt.subplots_adjust(bottom=0.4)  # 아래쪽 여백을 충분히 확보

        # 그래프를 이미지로 변환
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        deposit_image_png = buffer.getvalue()
        buffer.close()

        # base64 인코딩
        deposit_graphic = base64.b64encode(deposit_image_png)
        deposit_graphic = deposit_graphic.decode('utf-8')
    else:
        deposit_graphic = None

    # 그래프 이미지를 포함한 응답 반환
    context = {
        'save_graphic': save_graphic,
        'deposit_graphic': deposit_graphic,
    }

    return JsonResponse({
        'save_graphic': save_graphic,
        'deposit_graphic': deposit_graphic,
    })

########################################################################
# 정기 예금 상품 추천
def recommend_deposit(user_id, n_recommendations=10):
    # 사용자의 정보를 가져옵니다.
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None

    # 사용자가 이미 가입한 예금 상품 ID를 가져옵니다.
    user_deposit_ids = JoinDeposit.objects.filter(
        user=user
    ).values_list('product', flat=True)

    # 현재 사용자가 이미 가입한 상품을 제외
    # 각 상품에 대한 가입자 수를 세어 num_joins라는 새로운 필드로 추가
    # 현재 사용자와 같은 직업을 가진 다른 사용자들이 가입한 상품을 필터링
    # 현재 사용자와 같은 지역에 사는 다른 사용자들이 가입한 상품도 필터링
    # 가입자 수가 2 이하인 상품을 제외
    # 가입자 수가 많은 상품부터 정렬
    recommended_products_query = DepositProducts.objects \
        .exclude(id__in=user_deposit_ids) \
        .annotate(num_joins=Count('joindeposit')) \
        .filter(
            joindeposit__user__job=user.job,
            joindeposit__user__location=user.location
        ) \
        .exclude(num_joins__lte=2) \
        .order_by('-num_joins')[:n_recommendations]

    # 옵션 정보를 포함하여 추천 상품을 반환합니다.
    recommended_products = [
        {
            "product": product,
            "options": list(DepositOptions.objects.filter(product=product).values()),
            "num_joins" : product.num_joins,
            "fin_prdt_cd": product.fin_prdt_cd,
        }
        for product in recommended_products_query
    ]
    return recommended_products

# Vue로 출력하는 함수
def product_recommendations_deposit(request, user_id):
    if request.method == 'GET':
        recommendations_with_options = recommend_deposit(user_id)
        if recommendations_with_options:
            data = [{
                'product_name': item['product'].fin_prdt_nm,
                'details': item['product'].etc_note,
                'kor_co_nm': item['product'].kor_co_nm,
                'options': item['options'],
                'num_joins': item['num_joins'],
                'fin_prdt_cd': item['fin_prdt_cd'],
            } for item in recommendations_with_options]
            return JsonResponse({'products': data})
            # return JsonResponse({"dat": data})
        else:
            return JsonResponse({'error': 'No recommendations available'}, status=404)
##################
# 정기 적금 상품 추천
def recommend_save(user_id, n_recommendations=10):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None

    # 사용자가 이미 가입한 적금 상품 ID를 가져옵니다.
    user_savings_ids = JoinSave.objects.filter(
        user=user
    ).values_list('product', flat=True)

    # 현재 사용자가 이미 가입한 적금 상품을 제외
    # 각 상품에 대한 가입자 수를 세어 num_joins라는 새로운 필드로 추가
    # 현재 사용자와 같은 직업을 가진 다른 사용자들이 가입한 적금 상품을 필터링
    # 현재 사용자와 같은 지역에 사는 다른 사용자들이 가입한 적금 상품도 필터링
    # 가입자 수가 2 이하인 적금 상품을 제외
    # 가입자 수가 많은 적금 상품부터 정렬
    recommended_savings_query = SaveProducts.objects \
        .exclude(id__in=user_savings_ids) \
        .annotate(num_joins=Count('joinsave')) \
        .filter(
            joinsave__user__job=user.job,
            joinsave__user__location=user.location
        ) \
        .exclude(num_joins__lte=2) \
        .order_by('-num_joins')[:n_recommendations]

    # 옵션 정보를 포함하여 추천 적금 상품을 반환합니다.
    recommended_savings = [
        {
            "product": product,
            "options": list(SaveOptions.objects.filter(product=product).values()),
            "num_joins": product.num_joins,
            "fin_prdt_cd": product.fin_prdt_cd,
        }
        for product in recommended_savings_query
    ]
    return recommended_savings

# Vue로 출력하는 함수
def savings_recommendations_save(request, user_id):
    if request.method == 'GET':
        recommendations_with_options = recommend_save(user_id)
        if recommendations_with_options:
            data = [{
                'product_name': item['product'].fin_prdt_nm,
                'details': item['product'].etc_note,
                'kor_co_nm': item['product'].kor_co_nm,
                'options': item['options'],
                'num_joins': item['num_joins'],
                'fin_prdt_cd': item['fin_prdt_cd'],
            } for item in recommendations_with_options]
            return JsonResponse({'products': data})
            # return JsonResponse({"dat": data})

        else:
            return JsonResponse({'error': 'No recommendations available'}, status=404)
        
        
## 지역별 / 직업별 top3 상품 리턴
from django.db.models import Count
from django.http import JsonResponse


def top_deposits_by_location_and_job(request):
    location_counts = JoinDeposit.objects.values('user__location', 'product_id') \
        .annotate(selection_count=Count('product_id'))


    job_counts = JoinDeposit.objects.values('user__job', 'product_id') \
        .annotate(selection_count=Count('product_id'))

    # top3 찾기
    top_location_products = {}
    top_job_products = {}


    for entry in location_counts:
        location = entry['user__location']
        product_id = entry['product_id']
        count = entry['selection_count']


        if location not in top_location_products:
            top_location_products[location] = []


        top_location_products[location].append({'product_id': product_id, 'count': count})


    for entry in job_counts:
        job = entry['user__job']
        product_id = entry['product_id']
        count = entry['selection_count']


        if job not in top_job_products:
            top_job_products[job] = []


        top_job_products[job].append({'product_id': product_id, 'count': count})


    # sort후 top3
    top_location_products = {location: sorted(products, key=lambda x: x['count'], reverse=True)[:3]
                            for location, products in top_location_products.items()}


    top_job_products = {job: sorted(products, key=lambda x: x['count'], reverse=True)[:3]
                        for job, products in top_job_products.items()}


    response_data = {
        'top_location_products': top_location_products,
        'top_job_products': top_job_products,
    }


    return JsonResponse(response_data)


def top_saves_by_location_and_job(request):
    location_counts = JoinSave.objects.values('user__location', 'product_id') \
        .annotate(selection_count=Count('product_id'))


    job_counts = JoinSave.objects.values('user__job', 'product_id') \
        .annotate(selection_count=Count('product_id'))

    # top3 찾기
    top_location_products = {}
    top_job_products = {}


    for entry in location_counts:
        location = entry['user__location']
        product_id = entry['product_id']
        count = entry['selection_count']


        if location not in top_location_products:
            top_location_products[location] = []


        top_location_products[location].append({'product_id': product_id, 'count': count})


    for entry in job_counts:
        job = entry['user__job']
        product_id = entry['product_id']
        count = entry['selection_count']


        if job not in top_job_products:
            top_job_products[job] = []


        top_job_products[job].append({'product_id': product_id, 'count': count})


    # sort후 top3
    top_location_products = {location: sorted(products, key=lambda x: x['count'], reverse=True)[:3]
                            for location, products in top_location_products.items()}


    top_job_products = {job: sorted(products, key=lambda x: x['count'], reverse=True)[:3]
                        for job, products in top_job_products.items()}


    response_data = {
        'top_location_products': top_location_products,
        'top_job_products': top_job_products,
    }


    return JsonResponse(response_data)