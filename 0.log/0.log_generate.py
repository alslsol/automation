import os
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

local_file_path = '/home/ubuntu/damf2/data/logs/'
    # log 자동 생성 >> 생성시킬 위치 경로 설정

def generate_log_line(timestamp):
    ip = fake.ipv4()
    method = random.choice(['GET', 'POST'])

    if random.random() < 0.5:
        path = f'/product/{random.randint(1000, 9000)}'
    else:
        path = random.choice(['/index', '/login', '/contact'])

    protocol = 'HTTP/1.1'
    status_code = random.choice([200, 301, 400, 404, 500])
    response_size = random.randint(200, 5000)
    log_line = f'{ip} [{timestamp}] "{method} {path} {protocol}" {status_code} {response_size}'

    return log_line


def generate_logs(start_date, end_date):
    while start_date <= end_date:
        log_date_str = start_date.strftime('%Y-%m-%d')
        file_name = f'{log_date_str}.log'

        num_logs = random.randint(1000, 2000)

        logs = []

        for i in range(num_logs):
            log_timestamp = start_date + timedelta(seconds=random.randint(0, 86400))
            log_timestamp = log_timestamp.strftime('%Y-%m-%d:%H:%M:%S')
            log_line = generate_log_line(log_timestamp)
            logs.append(log_line)

        # '2024-08-05 05:00:22] "POST /product/3118 HTTP/1.1" 200 944'
        logs.sort(key=lambda x: x.split('[')[1].split(']')[0])

        if not os.path.exists(local_file_path):
            os.makedirs(local_file_path)

        with open(local_file_path + file_name, 'w', encoding='utf-8') as local_file:
            for log_line in logs:
                local_file.write(log_line + '\n')

        start_date += timedelta(days=1)


def get_last_log_date():
    files = os.listdir(local_file_path)
    files.sort()
    if not files:
        return datetime(2024, 1, 1)  # 기본 시작 날짜
    last_file = files[-1]
    last_date_str = last_file.split('.')[0]
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    return last_date

last_date = get_last_log_date()

start_date = datetime(last_date.year, last_date.month, last_date.day)
end_date = start_date + timedelta(days=1)


generate_logs(start_date, end_date)