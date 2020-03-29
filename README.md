## 카카오톡으로 채용 공고 알림 받기

### About
카카오톡 메신저로 채용 정보를 받는다. 채용 정보는 특정 대학교(본교)의 채용 알림 사이트에서 수집하며, 평일 08:05, 09:05에 알림 받는다. 
*(현재까지 편리하게 사용 중인 어플리케이션)*

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
  - token.txt

### Env
- Python 3
- Docker (on Ubuntu server)

### Docs
- URL

### Demo
- URL

### Date
- 2019.12.05 ~ 2019.12.12 (1 week)

<br>
최종 수정일: 2020-03-29
