# 네이버웹툰 크롤링
- 크롬 드라이버 사용
- BeautifulSoup으로 페이지 소스 파싱

------------------------------------------
- webtoon_data.csv : 월~일 까지 웹툰 정보
- webtoon_data_scrolled.csv : 월~일, 완결 웹툰 정보
- days,title,author,rating,url 순으로 정렬

### 스크롤 방식으로 현 네이버 웹툰 사이트 요일별 웹툰 보는 곳에서, 완결 웹툰의 경우 페이지 형식이 아닌 스크롤 형식으로 되어 있어서 스크롤을 내려가면서 크롤링 해오는 식으로 전체 웹툰 데이터 크롤링 진행
