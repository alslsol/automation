from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome()
URL = 'https://www.melon.com/chart/index.htm' # 경로 변수화
driver.get(URL)

# CSS 셀렉터 기준으로 요소 찾기
    # 셀레니움 find_element: 해당하는 요소 1개만 찾는 기능 -> elements 해야 해당하는 모든 것 출력
    # 로직: 차트에서 >> 첫번째 곡정보 클릭 후 뒤로 가서, 두번째 곡정보 클릭
song_info = driver.find_elements(By.CSS_SELECTOR, 'a.btn.song_info')
    # a태그인데, 클래스로 btn, song_info 가진 모든 요소 찾기

# print(song_info.get_attribute('title'))
    # song_info에는 html 코드 들어 있음 -> 그중 title에 해당하는 내용만 출력

# print(len(song_info))
    # 총 몇개의 해당 요소 있는지 개수 출력

song_list = []

# 0-5번째까지 차트 곡 중, song_info 버튼 클릭
for i in range(5):
    # 순서대로 song_info 버튼 클릭 >> 해당 페이지 들어가기
    song_info[i].click()
    time.sleep(2) # 한번 클릭한 뒤 2초 기다린 뒤 다시 for문 반복
        # 로딩 다 돼야 버튼/요소 찾을 수 있음 >> 화면 로딩 긴 사이트의 경우 sleep 오래 둬야 함

    # 곡 정보 페이지에서 >> 곡 제목, 가수, 좋아요 수 수집하기
    title = driver.find_element(By.CSS_SELECTOR, 'div.song_name').text
        # 개발자 도구로 html 코드 확인해 규칙 찾은 뒤 >> 수집 작업만 자동화 하는 식
        # div 태그에 song_name 클래스 붙은 것 찾은 뒤 >> text만 추출

    # 가수 정보 가져오기
    artist = driver.find_element(By.CSS_SELECTOR, 'div.artist span').text
        # 클래스 artist 가진 div 아래의 후손 중 하나인 span태그 고르기 -> find_element 이므로 첫번째 span만 출력됨

    # 발매일 가져오기: 근데 같은 위치에 dd 태그 4개 있고, 우리가 가져올 건 그 중 2번째임
    # 방법1) 여러개 찾은 다음 하나에 접근하기
    meta_data = driver.find_elements(By.CSS_SELECTOR, 'div.meta dd')
    # print(meta_data[1].text)
        # 해당 메타 데이터의 1번째에 접근 >> 해당 데이터의 텍스트 출력 -> 그러면 5개 곡의 발매일 출력 가능
    # 방법2) 
    publish_date = driver.find_element(By.CSS_SELECTOR, 'dl.list > dd:nth-of-type(2)').text
        # list 클래스 가진 dl 선택 > 그 자식 요소인 dd 중 2번째 요소 선택

    # 좋아요 수 가져오기
    like_cnt = driver.find_element(By.CSS_SELECTOR, 'span#d_like_count').text
        # id 달려 있는 경우 #으로 찾기 가능 -> span 태그 중 d_like_count id 달린 요소 찾기
    like_cnt = like_cnt.replace(',', '') # 쉼표 지우기 >> 데이터 수집 과정에서 데이터 정제하기
        # 데이터 정제

    song_list.append([title, artist, publish_date, like_cnt])

    # 뒤로 나와서 차트로 돌아가기
    driver.back() # 크롬 브라우저에서 뒤로 가기 버튼 누른단 것


# 크롤링 정보 csv로 저장
local_file_path = '/home/ubuntu/damf2/data/melon/' # 로컬 어디에 저장할지 경로 변수화

def save_to_csv(song_list):
    with open(local_file_path + 'melon-top-100.csv', 'w', encoding='utf-8') as file:
            # open: 파일 여는 함수 >> 해당 경로에 melon-top-100.csv 파일 생성
            # w: 쓰기 모드로 변경
            # 한글 섞여 있으므로 인코딩 방식 지정
        writer = csv.writer(file)
        writer.writerows(song_list)
            # writerows: 여러 줄 동시에 csv로 변경
save_to_csv(song_list)