# 88개 크롤링 성공했던 평행우주로 회귀.. 근데 안됨;;
# 근데 click마다 timesleep 줬더니 좀 나아진듯 >> 근데 다시 문제: 무한루프 빠짐;; 1-2페이지만 계속 돌아감 설레다 말았네

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv, re

# 셀레니움 드라이버 설정
driver = webdriver.Chrome()
URL = 'https://likms.assembly.go.kr/bill/BillSearchProposalResult.do'
driver.get(URL)

# 1. 키워드 입력 함수
    # 전체 의안 중 디지털 성범죄 등 키워드 검색
def search_keyword(keyword):
    # 키워드 입력
    search_input = driver.find_element(By.ID, 'query')
    search_input.send_keys(keyword)

    # 엔터로 검색 버튼 누르기
    search_input.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")))

# 2. 데이터 수집 함수
def collect_data():
    laws = [['의안번호', '의안명', '제안이유 및 주요내용']]
    
    while True:
        try:
            links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
            total_links = len(links)

            for i in range(total_links):
                try:
                    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
                    link = links[i]

                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    link.click()
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.subContents h3.titCont'))
                    )

                    head = driver.find_element(By.CSS_SELECTOR, 'div.subContents > h3.titCont').text
                    match = re.match(r'\[(\d+)\]\s*(.+)', head)
                    if match:
                        number = match.group(1)
                        title = match.group(2)

                    body = driver.find_element(By.CSS_SELECTOR, 'div.contIn div.textType02').text
                    body = clean_text(body)

                    laws.append([number, title, body])

                    driver.back()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                    )

                except Exception as e:
                    print(f"[{i+1}/{total_links}] 링크 클릭 시도 중...")
                    print(f'링크 처리 중 에러 발생: {e}')
                    driver.back()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                    )
                    continue

        except Exception as e:
            print(f'페이지 전체 처리 중 에러: {e}')
        
        # 다음 페이지 시도
        if not go_to_next_page():
            break

    return laws

# 3. 페이지 이동 함수
current_page = 0
def go_to_next_page():
    global current_page
    try:
        # 숫자 버튼 찾기
        btns = driver.find_elements(By.CSS_SELECTOR, 'a[href="#none"][onclick^="javascript:goPage"]')

        for btn in btns:
            onclick_val = btn.get_attribute('onclick')
            btn_class = btn.get_attribute('class')

            # goPage 속에 10, 20, 30 있는데 그 숫자 추출
            match = re.search(r"goPage\('(\d+)'\)", onclick_val)

            if match: # match와 같은 패턴인 경우
                page_num = int(match.group(1))

                if page_num > current_page:
                    print(f'{current_page}에서 {page_num}로 이동 중')

                    btn.click()
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                    )
                    current_page = page_num
                    return True
        return False # 매치랑 다른 경우 False

    except Exception as e:
        print(f'{page_num}으로 페이지 이동 중 오류 발생: {e}')
        return False

# 4. 텍스트 정제 함수
def clean_text(text):
    # 무엇을, 어떻게 정제할지
    replace_dict = {
                '\n': ' ',
                '제안이유 및 주요내용': '',
                'ㆍ': '·',
                '[': '',
                ']': '',
            }
    # 데이터 정제
    for old, new in replace_dict.items():
        text = text.replace(old, new)
    return text

# 5. csv 파일 저장 함수
local_file_path = '/home/ubuntu/damf2/data/temp/'

def save_to_csv(laws):
    with open(local_file_path + '디지털 성범죄.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(laws)
        print(f'데이터 저장 완료')


# 실행
def main():
    search_keyword('디지털 성범죄')
    laws = collect_data()
    save_to_csv(laws)

if __name__ == "__main__":
    main()
    driver.quit()

######성ㄱ오라옥오가ㅣ이!!!