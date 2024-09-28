import API
import module.back1 as back1
import requests
import json
from datetime import datetime, timedelta
import time

# python -m venv 가상환경이름 <== 가상환경 생성
# cd stockk\Scripts
# activate.bat
# deactivate

# pip freeze > requirements.txt
# pip install -r requirements.txt

# API.id, API.pw, API.account_number_front, API.account_number_back, API.URL_BASE, API.KEY, API.SECRET

ACCESS_TOKEN = API.temp_token


def get_last_run_time():
    try:
        with open('last_run.json', 'r') as file:
            data = json.load(file)
            return datetime.fromisoformat(data['last_run'])
    except (FileNotFoundError, KeyError):
        return None

def update_last_run_time():
    with open('last_run.json', 'w') as file:
        json.dump({'last_run': datetime.now().isoformat()}, file)

while True:
    try:
        # 1일마다 체크해서 토큰을 재발급받는 코드
        last_run = get_last_run_time()
        now = datetime.now()

        if (last_run is None) or (now >= last_run + timedelta(days=1)):
            ACCESS_TOKEN = back1.get_access_token(API.KEY, API.SECRET, API.URL_BASE)
            update_last_run_time()
        # 1일마다 체크해서 토큰을 재발급받는 코드

        showmethemoney = back1.get_balance(API.URL_BASE, ACCESS_TOKEN, API.KEY, API.SECRET, API.account_number_front, API.account_number_back)
        print(showmethemoney)
        time.sleep(1)
    except Exception as e:
        print(f"[오류 발생]{e}")
        time.sleep(1)