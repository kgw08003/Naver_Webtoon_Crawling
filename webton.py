# 완결 웹툰 미포함
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import pandas as pd
# import time

# # ChromeDriver 경로 설정
# chrome_driver_path = "C:/Users/kgw08/Downloads/chromedriver-win64/chromedriver.exe"  # 또는 이스케이프 시퀀스 사용
# service = Service(chrome_driver_path)

# # 브라우저 열기
# driver = webdriver.Chrome(service=service)
# h = 'https://comic.naver.com/webtoon/weekdayList?week='
# day = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'dailyplus', 'new', 'finish']
# df = pd.DataFrame(columns=['days', 'title', 'author', 'rating', 'url'])

# for i in day:
#     driver.get(h + i)
#     time.sleep(2)  # 페이지 로딩 대기

#     # BeautifulSoup으로 페이지 소스 파싱
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # 웹툰 리스트 가져오기
#     data = soup.find('ul', {'class': 'ContentList__content_list--q5KXY'})
#     if data is None:
#         print(f"'{i}' 페이지에서 'ContentList__content_list--q5KXY' 클래스를 찾을 수 없습니다.")
#         continue

#     items = data.findAll('li', {'class': 'item'})
#     days = i

#     for item in items:
#         # 웹툰 제목 가져오기
#         title_element = item.find('span', {'class': 'text'})   # 클래스명 확인 필요
#         title = title_element.text.strip() if title_element else '제목 없음'
        
#         # 저자 정보 가져오기
#         author_element = item.find('a', class_='ContentAuthor__author--CTAAP')  # 클래스명 확인 필요
#         author = author_element.text.strip() if author_element else '저자 정보 없음'
        
#         # 평점 정보 가져오기
#         rating_element = item.find('span', class_='Rating__star_area--dFzsb')   # 클래스명 확인 필요
#         rating = rating_element.text.strip().replace('별점', '').strip() if rating_element else 'N/A'
        
#         # URL 가져오기
#         url = 'https://comic.naver.com' + item.find('a')['href']

#         # 데이터프레임에 추가
#         df = pd.concat([df, pd.DataFrame([[days, title, author, rating, url]],
#                                          columns=['days', 'title', 'author', 'rating', 'url'])])

# # 브라우저 닫기
# driver.quit()

# # CSV 파일로 저장
# df.to_csv('webtoon_data.csv', index=False, encoding='utf-8-sig')

# # 결과 출력
# print(df)


# 스크롤 방식으로 현 네이버 웹툰 사이트 요일별 웹툰 보는 곳에서, 완결 웹툰의 경우 페이지 형식이 아닌 스크롤 형식으로 되어 있어서 
# 스크롤을 내려가면서 크롤링 해오는 식으로 전체 웹툰 데이터 크롤링 진행
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# ChromeDriver 경로 설정
chrome_driver_path = "C:/Users/kgw08/Downloads/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)

# 브라우저 열기
driver = webdriver.Chrome(service=service)
h = 'https://comic.naver.com/webtoon/weekdayList?week='
day = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'dailyplus', 'new', 'finish']
df = pd.DataFrame(columns=['days', 'title', 'author', 'rating', 'url'])

for i in day:
    driver.get(h + i)
    time.sleep(2)  # 페이지 로딩 대기

    last_height = driver.execute_script("return document.body.scrollHeight")  # 현재 문서 높이

    while True:
        # 페이지 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 페이지 로딩 대기
        
        # 새로운 문서 높이를 가져오기
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 더 이상 스크롤이 불가능하면 종료
        if new_height == last_height:
            break
        last_height = new_height

    # BeautifulSoup으로 페이지 소스 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 웹툰 리스트 가져오기
    data = soup.find('ul', {'class': 'ContentList__content_list--q5KXY'})
    if data is None:
        print(f"'{i}' 페이지에서 'ContentList__content_list--q5KXY' 클래스를 찾을 수 없습니다.")
        continue

    items = data.findAll('li', {'class': 'item'})
    
    for item in items:
        # 웹툰 제목 가져오기
        title_element = item.find('span', {'class': 'text'})
        title = title_element.text.strip() if title_element else '제목 없음'

        # 저자 정보 가져오기
        author_element = item.find('a', class_='ContentAuthor__author--CTAAP')
        author = author_element.text.strip() if author_element else '저자 정보 없음'

        # 평점 정보 가져오기
        rating_element = item.find('span', class_='Rating__star_area--dFzsb')
        rating = rating_element.text.strip().replace('별점', '').strip() if rating_element else 'N/A'

        # URL 가져오기
        url = 'https://comic.naver.com' + item.find('a')['href']

        # 데이터프레임에 추가
        df = pd.concat([df, pd.DataFrame([[i, title, author, rating, url]],
                                         columns=['days', 'title', 'author', 'rating', 'url'])], ignore_index=True)

# 브라우저 닫기
driver.quit()

# CSV 파일로 저장
df.to_csv('webtoon_data_scrolled.csv', index=False, encoding='utf-8-sig')

# 결과 출력
print(df)
