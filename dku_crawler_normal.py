import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd

headers = {'Referer': 'https://portal.dankook.ac.kr/web/portal', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
data1 = {'username': '@user_id', 'password': '@user_pwd'}
data2 = {'userId': '@user_id', 'rtnUrl': ''}

loginTry_url_post_1 = "https://webinfo.dankook.ac.kr/member/logon.do?sso=ok"
loginTry_url_get_1 = "https://youngwoong.dankook.ac.kr/common/user/dialog/sso/ssocheck.do?rtnUrl=null"
loginTry_url_post_2 = "https://youngwoong.dankook.ac.kr/common/user/loginProc.do"

base_url = "ptfol/empymn/general/findRecomendMngtView.do?"  # It's used to create href.
page_url = "https://youngwoong.dankook.ac.kr/ptfol/empymn/general/findRecomendMngtList.do?paginationInfo.currentPageNo={}" # It's used to crawl target site.

def crawler_dkujob_normal():
    _result_code = 0;
    _result = [];

    with requests.Session() as session:
        ''' for login '''
        print(">"*60 + "login try 1 ok ... (post)")
        html = session.post(loginTry_url_post_1, data = data1)

        print(">" * 60 + "login try 2 ok ... (get)")
        html = session.get(loginTry_url_get_1)

        print(">" * 60 + "login try 3 ok ... (post)")
        html = session.post(loginTry_url_post_2, data=data2)

        ''' for scraping '''
        print(">" * 60 + "start scraping ...")
        # for-loop
        for page in range(1, 31):   # 5 to 31
            print(page,"of 30 page")
            html = session.get(page_url.format(page))
            soup = bs(html.text, "lxml"); # print(soup)
            post_list = soup.select('div.tableType01 tbody tr')
            post_cnt = 0
            for post in post_list:
                attr_list = post.select('td')
                _number = attr_list[0].text.strip()
                _campus = attr_list[1].text.strip()
                _area = attr_list[2].text.strip()
                _company = attr_list[3].text.strip()
                _main = attr_list[4].select('a')[0] # not using.
                _title = _main.text.strip()
                _href = _main['data-params']
                _href = _href[1:-1] # cut {, }.
                _href = (base_url + _href.split(':')[0].replace('"', '') + '=' + _href.split(':')[1].replace('"', ''))   # make url.
                _status = attr_list[5].text.strip()
                _r_date = attr_list[6].text.strip() # registration date
                _d_date = attr_list[7].text.strip() # deadline date

                if _status == "마감":
                    continue
                else:
                    # print(_number,_campus, _area, _company, _title, _href, _status, _r_date, _d_date)
                    post_cnt = post_cnt + 1
                    _result.append((_number,_campus, _area, _company, _title, _href, _status, _r_date, _d_date))
            # print(page,"page scraped post number >", post_cnt, end="\n")
        print("total scraped posts >> {}".format(len(_result)))
        print(">" * 60 + "finish scraping ...")
    return _result_code, _result;

if __name__ == '__main__':
    print(">")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    _result_code, _result = crawler_dkujob_normal()
    if _result_code == -1:
        print("Error crwaling")

    # Handling Data Frame
    names = ["Number", "Campus", "Area", "Company", "Title", "Href", "Status", "R_date", "D_date"]
    _result_df = pd.DataFrame(_result, columns=names)
    _result_df.to_csv('./data/posts.csv',index=False, mode='w', encoding='utf-8')
