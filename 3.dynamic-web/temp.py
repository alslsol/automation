from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv, re


driver = webdriver.Chrome()
URL = 'https://likms.assembly.go.kr/bill/BillSearchProposalResult.do'
driver.get(URL)

# 전체 의안 중, 디지털 성범죄 키워드 검색
# 키워드 입력
search_input = driver.find_element(By.ID, 'query')
search_input.send_keys('디지털 성범죄')
# 엔터로 검색 버튼 누르기
search_input.send_keys(Keys.RETURN)
time.sleep(2)

laws = [['의안번호', '의안명', '제안이유 및 주요내용']]

links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
# print(len(links))

# 하나씩 상세 페이지 들어갔다가 >> 수집하고 >> 뒤로 돌아오기
for i in range(len(links)):
    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
    driver.execute_script("arguments[0].scrollIntoView(true);", links[i])
    time.sleep(1)

    # 링크 클릭해 상세 페이지 들어가기
    links[i].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.subContents h3.titCont"))  # 페이지 로딩 기다리기
    )

    # 데이터 수집하기
    # 1) 의안명
    head = driver.find_element(By.CSS_SELECTOR, 'div.subContents > h3.titCont').text
    match = re.match(r'\[(\d+)\]\s*(.+)', head)
    if match:
        number = match.group(1)
        title = match.group(2)

    # 2) 제안이유
    body = driver.find_element(By.CSS_SELECTOR, 'div.contIn div.textType02').text

    replace_dict = {
        '\n': ' ',
        '제안이유 및 주요내용': '',
        'ㆍ': '·',
        '[': '',
        ']': '',
    }

    for old, new in replace_dict.items():
        body = body.replace(old, new)

    # body = body.replace('\n', ' ')
    # body = body.replace('제안이유 및 주요내용', '')
    # body = body.replace('ㆍ', '·')

    laws.append([number, title, body])

    # 뒤로 돌아가기
    driver.back()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
    )

print(laws)
print(len(laws))

# csv 파일로 저장
local_file_path = '/home/ubuntu/damf2/data/temp/'

def save_to_csv(laws):
    with open(local_file_path + '디지털 성범죄.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(laws)
save_to_csv(laws)