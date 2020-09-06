## 카카오톡으로 채용 공고 알림 받기

<br>

### About
카카오톡 메신저로 채용 정보를 받는다.<br>
채용 정보는 본교의 채용 알림 사이트에서 수집하며, 평일 08:05, 09:05에 알림 받는다. 

<br>

### Files
**`./` 폴더**
- 데이터 수집
  - `dku_crawler_internship.py`
  - `dku_crawler_normal.py`
- 데이터 전송 (카카오톡)
  - `dku_crawler_internship_kakaotalk.py`
  - `dku_crawler_normal_kakaotalk.py`


**`/data` 폴더**
- 수집된 데이터
  - `internship_posts.csv`
  - `normal_posts.csv`
- 전송된 데이터
  - `known_internship_posts.txt`
  - `known_normal_posts.txt`
- 토큰 (카카오 API)
  - `token.txt`

<br>

### Env
- Python 3
- Docker (on linux server)

<br>

### Example 1
- <img src="./image/example02.png" width="40%" height="40%">

### Example 2
- <img src="./image/example01.jpg" width="40%" height="40%">

### Example 3
- http://hj2server.ddns.net/files/portfolio_hj-dkujob-scrapping.pdf

<br>

### Date
- 2019.12.05 ~ 2019.12.12 (1 week)

<br>

### 개선 사항
- 리팩토링
  - 모듈화
  - 주석 통일
  - 파일 정리
  - 네이밍

<br>
최종 수정일: 2020-09-07
