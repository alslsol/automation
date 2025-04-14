import requests
from bs4 import BeautifulSoup

# 응답 가져오기
lotto_url = 'https://dhlottery.co.kr/common.do?method=main'
res = requests.get(lotto_url)

soup = BeautifulSoup(res.text, 'html.parser') # html 파일이므로, html.parser 사용하라고 지정
    # soup으로 한번 묶으면, 내가 원하는 것 찾는 기능 쓸 수 있음

balls = soup.select('span.ball_645')
    # select: 해당 조건 맞는 모든 데이터 리스트로 묶어서 전달

# 찾은 balls 중, text 정보(당첨번호)만 추출
for ball in balls:
    print(ball.text)