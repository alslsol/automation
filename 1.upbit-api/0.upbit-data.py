from datetime import datetime
import requests
import time
import csv

upbit_url = 'https://api.upbit.com/v1/ticker?markets=KRW-BTC'

# 시작 시간 설정
start_time = time.time()

bit_data_list = [] # 데이터 넣을 공용 공간

# 최신 시간 - 설정한 시간이 60초 넘을 때 멈추도록
while time.time() - start_time < 60:
    res = requests.get(upbit_url) # url 입력 시 응답값 넣기
    data = res.json()[0] # json을 dict으로 변환

    bit_data = [
        data['market'],
        data['trade_date'], # dict 응답값 중 일부만 추출
        data['trade_time'],
        data['trade_price']
    ]
    bit_data_list.append(bit_data)
    time.sleep(20) # 5초에 한번씩 요청 보내고, 1분 지나면 요청 그만 보낼 것

# 로컬에 파일 저장 후 통채로 hdfs에 올리기
local_file_path = '/home/ubuntu/damf2/data/bitcoin/'
now = datetime.now() # 현재 시간 저장
file_name = now.strftime('%H-%M-%S') + '.csv' # 데이트타임 객체를 글자로 만들어줌 >> 시-분-초 형태의 문자열로 변환
    # 파일 생성 >> 이후 bit_data 파일에 밀어넣기

# 파일 열고, with문 살아 있는 동안 그 내부에서 file 변수 살아 있음
with open(local_file_path + file_name, mode='w', newline='') as file:
    writer = csv.writer(file) # 내가 쓰고 싶은 파일 열기
    writer.writerows(bit_data_list) # 여러 줄 데이터 동시에 열기