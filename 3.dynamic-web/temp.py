from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
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
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")))

    # 엔터로 검색 버튼 누르기
    search_input.send_keys(Keys.RETURN)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")))

# 2. 데이터 수집 함수
def collect_data():
    laws = [['의안번호', '의안명', '제안이유 및 주요내용']]

    while True:
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
        total_links_count = len(links)

        if not links:
            print('더 이상 수집할 링크가 없습니다')
            break

        # index 접근을 해야 오류 줄일 수 있음
        for i in range(total_links_count): # 링크 하나씩 꺼내기 >> 클릭 >> 상세 페이지 이동
            success = False
            retry_count = 0
            while not success and retry_count < 3:
                try:
                    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']")
                    link = links[i]

                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    link.click() # 링크 클릭해 상세 페이지 들어가기
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.subContents h3.titCont'))
                    ) # 로딩 기다리기

                    # 데이터 수집
                    # 1) 의안명
                    head = driver.find_element(By.CSS_SELECTOR, 'div.subContents > h3.titCont').text
                    match = re.match(r'\[(\d+)\]\s*(.+)', head)
                    if match:
                        number = match.group(1)
                        title = match.group(2)

                    # 2) 제안이유
                    body = driver.find_element(By.CSS_SELECTOR, '#summaryContentDiv').text
                    body = clean_text(body) # 이후 데이터 정제 함수 만들어서 돌릴 것
                    
                    # laws 리스트에 추가하기
                    laws.append([number, title, body])

                    # 수집 다 했으면, 뒤로 돌아가기
                    driver.back()
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                    )
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f'재시도 중 에러 발생 (시도 {retry_count+1}): {e}')
                    retry_count += 1
                    time.sleep(1)  # 약간의 시간 텀 주기
                    continue
                except Exception as e:
                    print(f'기타 오류 발생: {e}')
                    break
                finally:
                    # 페이지 뒤로 가기 (데이터 수집 시도 여부와 상관없이)
                    driver.back()
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                    )
        
        # 다음 페이지 넘어가기 >> 없으면 중단
        if not go_to_next_page():
            break

    return laws

# 3. 텍스트 정제 함수
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

# 4. 페이지 이동 함수
def go_to_next_page():
    try:
        # 숫자 버튼 찾기
        btns = driver.find_elements(By.CSS_SELECTOR, 'a[href="#none"][onclick^="javascript:goPage"]')

        for btn in btns:
            onclick_val = btn.get_attribute('onclick')
            btn_class = btn.get_attribute('class')

            # goPage 속에 10, 20, 30 있는데 그 숫자 추출
            match = re.search(r"goPage\('(\d+)'\)", onclick_val)

            if match: # match와 같은 패턴인 경우
                page_num = match.group(1)
                btn.click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='javascript:fGoDetail']"))
                )
                return True
        return False # 매치랑 다른 경우 False
    except Exception as e:
        print(f'페이지 이동 중 오류 발생: {e}')
        return False

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