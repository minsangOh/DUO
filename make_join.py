import random
import json
import os

def generate_save_data(length):
    save_data = []
    user_product_set = set()

    for i in range(length):
        user = random.randint(1, 10000)
        product = random.randint(1, 62)

        while (user, product) in user_product_set:
            user = random.randint(1, 10000)
            product = random.randint(1, 62)

        user_product_set.add((user, product))

        save_data.append({
            'model': 'apis.JoinSave',
            'pk': i + 1,
            'fields': {
                'user': user,
                'product': product,
            }
        })

    return save_data

def generate_deposit_data(length):
    deposit_data = []
    user_product_set = set()

    for i in range(length):
        user = random.randint(1, 10000)
        product = random.randint(1, 38)

        while (user, product) in user_product_set:
            user = random.randint(1, 10000)
            product = random.randint(1, 38)

        user_product_set.add((user, product))

        deposit_data.append({
            'model': 'apis.JoinDeposit',
            'pk': i + 1,
            'fields': {
                'user': user,
                'product': product,
            }
        })

    return deposit_data


join_save_data = generate_save_data(50000)
join_deposit_data = generate_deposit_data(50000)

save_dir1 = './back/apis/fixtures/apis/join_save_data.json'
os.makedirs(os.path.dirname(save_dir1), exist_ok=True)
with open(save_dir1, 'w', encoding='utf-8') as f:
    json.dump(join_save_data, f, ensure_ascii=False, indent=2)
print(f'데이터 생성 완료 / 저장 위치: {save_dir1}')


save_dir2 = './back/apis/fixtures/apis/join_deposit_data.json'
os.makedirs(os.path.dirname(save_dir2), exist_ok=True)
with open(save_dir2, 'w', encoding='utf-8') as f:
    json.dump(join_deposit_data, f, ensure_ascii=False, indent=2)
print(f'데이터 생성 완료 / 저장 위치: {save_dir2}')
