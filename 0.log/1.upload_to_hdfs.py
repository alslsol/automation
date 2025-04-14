from hdfs import InsecureClient
import os # 운영체제 컨트롤 가능한 라이브러리

client = InsecureClient('http://localhost:9870', user='ubuntu')
    # 하둡 링크, 컴퓨터 이름

# input 폴더 내 logs 폴더 만들기
# client.makedirs('/input/logs')

# 경로 변수화
local_file_path = '/home/ubuntu/damf2/data/logs/' # 리눅스 컴퓨터 내 로그 파일 저장된 경로
hdfs_file_path = '/input/logs/' # log 파일 어디에 업로드 할 건지

local_files = os.listdir(local_file_path)

for file_name in local_files:
    if not client.content(hdfs_file_path + file_name, strict=False):
        client.upload(hdfs_file_path + file_name, local_file_path + file_name)
        # 어디로 올릴지, 어디에 있는지