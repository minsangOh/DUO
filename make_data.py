import random
import requests
import json
from collections import OrderedDict
import os
from django.contrib.auth.hashers import make_password
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_pjt_back.settings')
django.setup()


first_name_samples = "김이박최정강조윤장임"
middle_name_samples = "민서예지도하주윤채현지"
last_name_samples = "준윤우원호후서연아은진"

location = [
    {
      "name": "서울특별시",
      "countries": [
        "강남구",
        "강동구",
        "강북구",
        "강서구",
        "관악구",
        "광진구",
        "구로구",
        "금천구",
        "노원구",
        "도봉구",
        "동대문구",
        "동작구",
        "마포구",
        "서대문구",
        "서초구",
        "성동구",
        "성북구",
        "송파구",
        "양천구",
        "영등포구",
        "용산구",
        "은평구",
        "종로구",
        "중구",
        "중랑구"
      ]
    },
    {
      "name": "부산광역시",
      "countries": [
        "강서구",
        "금정구",
        "기장군",
        "남구",
        "동구",
        "동래구",
        "부산진구",
        "북구",
        "사상구",
        "사하구",
        "서구",
        "수영구",
        "연제구",
        "영도구",
        "중구",
        "해운대구"
      ]
    },
    {
      "name": "대구광역시",
      "countries": [
        "남구",
        "달서구",
        "달성군",
        "동구",
        "북구",
        "서구",
        "수성구",
        "중구"
      ]
    },
    {
      "name": "인천광역시",
      "countries": [
        "강화군",
        "계양구",
        "남구",
        "남동구",
        "동구",
        "부평구",
        "서구",
        "연수구",
        "옹진군",
        "중구"
      ]
    },
    {
      "name": "광주광역시",
      "countries": ["광산구", "남구", "동구", "북구", "서구"]
    },
    {
      "name": "대전광역시",
      "countries": ["대덕구", "동구", "서구", "유성구", "중구"]
    },
    {
      "name": "울산광역시",
      "countries": ["남구", "동구", "북구", "울주군", "중구"]
    },
    {
      "name": "경기도",
      "countries": [
        "가평군",
        "고양시 덕양구",
        "고양시 일산동구",
        "고양시 일산서구",
        "과천시",
        "광명시",
        "광주시",
        "구리시",
        "군포시",
        "김포시",
        "남양주시",
        "동두천시",
        "부천시 소사구",
        "부천시 오정구",
        "부천시 원미구",
        "성남시 분당구",
        "성남시 수정구",
        "성남시 중원구",
        "수원시 권선구",
        "수원시 영통구",
        "수원시 장안구",
        "수원시 팔달구",
        "시흥시",
        "안산시 단원구",
        "안산시 상록구",
        "안성시",
        "안양시 동안구",
        "안양시 만안구",
        "양주시",
        "양평군",
        "여주군",
        "연천군",
        "오산시",
        "용인시 기흥구",
        "용인시 수지구",
        "용인시 처인구",
        "의왕시",
        "의정부시",
        "이천시",
        "파주시",
        "평택시",
        "포천시",
        "하남시",
        "화성시"
      ]
    },
    {
      "name": "강원도",
      "countries": [
        "강릉시",
        "고성군",
        "동해시",
        "삼척시",
        "속초시",
        "양구군",
        "양양군",
        "영월군",
        "원주시",
        "인제군",
        "정선군",
        "철원군",
        "춘천시",
        "태백시",
        "평창군",
        "홍천군",
        "화천군",
        "횡성군"
      ]
    },
    {
      "name": "충청북도",
      "countries": [
        "괴산군",
        "단양군",
        "보은군",
        "영동군",
        "옥천군",
        "음성군",
        "제천시",
        "증평군",
        "진천군",
        "청원군",
        "청주시 상당구",
        "청주시 흥덕구",
        "충주시"
      ]
    },
    {
      "name": "충청남도",
      "countries": [
        "계룡시",
        "공주시",
        "금산군",
        "논산시",
        "당진시",
        "보령시",
        "부여군",
        "서산시",
        "서천군",
        "아산시",
        "연기군",
        "예산군",
        "천안시 동남구",
        "천안시 서북구",
        "청양군",
        "태안군",
        "홍성군"
      ]
    },
    {
      "name": "전라북도",
      "countries": [
        "고창군",
        "군산시",
        "김제시",
        "남원시",
        "무주군",
        "부안군",
        "순창군",
        "완주군",
        "익산시",
        "임실군",
        "장수군",
        "전주시 덕진구",
        "전주시 완산구",
        "정읍시",
        "진안군"
      ]
    },
    {
      "name": "전라남도",
      "countries": [
        "강진군",
        "고흥군",
        "곡성군",
        "광양시",
        "구례군",
        "나주시",
        "담양군",
        "목포시",
        "무안군",
        "보성군",
        "순천시",
        "신안군",
        "여수시",
        "영광군",
        "영암군",
        "완도군",
        "장성군",
        "장흥군",
        "진도군",
        "함평군",
        "해남군",
        "화순군"
      ]
    },
    {
      "name": "경상북도",
      "countries": [
        "경산시",
        "경주시",
        "고령군",
        "구미시",
        "군위군",
        "김천시",
        "문경시",
        "봉화군",
        "상주시",
        "성주군",
        "안동시",
        "영덕군",
        "영양군",
        "영주시",
        "영천시",
        "예천군",
        "울릉군",
        "울진군",
        "의성군",
        "청도군",
        "청송군",
        "칠곡군",
        "포항시 남구",
        "포항시 북구"
      ]
    },
    {
      "name": "경상남도",
      "countries": [
        "거제시",
        "거창군",
        "고성군",
        "김해시",
        "남해군",
        "밀양시",
        "사천시",
        "산청군",
        "양산시",
        "의령군",
        "진주시",
        "창녕군",
        "창원시 마산합포구",
        "창원시 마산회원구",
        "창원시 성산구",
        "창원시 의창구",
        "창원시 진해구",
        "통영시",
        "하동군",
        "함안군",
        "함양군",
        "합천군"
      ]
    },
    {
      "name": "제주도",
      "countries": ["서귀포시", "제주시"]
    },
    {
      "name": "세종시",
      "countries": ["세종시"]
    }
]

job_data = [
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

def random_name(existing_usernames_set):
    while True:
        result = ""
        result += random.choice(first_name_samples)
        result += random.choice(middle_name_samples)
        result += random.choice(last_name_samples)
        new_name = result + str(random.randint(1, 100))
        
        if new_name not in existing_usernames_set:
            existing_usernames_set.add(new_name)
            return new_name



# json 파일 만들기
file = OrderedDict()

username_list = []
N = 200

# set 사용
username_set = set()

# 데이터 생성 부분 수정
i = 0
while i < N:
    rn = random_name(username_set)
    i += 1

def generate_dummy_data():
    data = []

    for i in range(200):
        location_data = random.choice(location)
        location_name = location_data['name']
        location_countries = location_data['countries']
        selected_country = random.choice(location_countries)

        location_str = f"{location_name} {selected_country}"

        username = random_name(username_set)
        hashed_password = make_password('1234')

        firstname = username[:1]
        lastname = username[1:3]
        age = random.randint(1, 100)
        money = random.randrange(0, 100000000, 100000)
        salary = random.randrange(0, 20000000, 1000000)  # 월급 2000만원 이하로 설정
        job = random.choice(job_data)

        user_data = {
            'model': 'accounts.user',
            'pk': i + 1,
            'fields': {
                'username': username,
                'first_name': firstname,
                'last_name': lastname,
                'age': age,
                'money': money,
                'salary': salary,
                'job': job[0],
                'location': location_str,
                'password': hashed_password,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
            }
        }

        data.append(user_data)

    return data

dummy_data = generate_dummy_data()

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = './back/accounts/fixtures/accounts/user_data.json'
os.makedirs(os.path.dirname(save_dir), exist_ok=True)

with open(save_dir, 'w', encoding='utf-8') as f:
    json.dump(dummy_data, f, ensure_ascii=False, indent=2)

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')