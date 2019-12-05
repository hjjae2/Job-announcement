import requests
import json
import pandas as pd
import datetime

def getAccessToken(refreshToken):
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=refresh_token&client_id=@my_client_id&refresh_token=" + refreshToken
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    reponse = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(reponse.text)
    return access_token

def exec_campusmon_post():
    file_path = "./data/posts.csv"
    names = ["Number", "Campus", "Area", "Company", "Title", "Href", "Status", "R_date", "D_date"]
    df = pd.read_csv(file_path)
    print(df.loc[:,"Title"])
    return df

def kakao_send_to_me(number, campus, area, company, title, href, status, r_date, d_date, KAKAO_TOKEN=""):
    header = {"Authorization":"Bearer " + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v2/api/talk/memo/send"
    description = []
    idx = 0
    while(idx < 5):
        if title[idx] != None:
            description.append(str(area[idx] + " / " + status[idx] + " / " + d_date[idx]))
        else:
            description.append(None)
        idx += 1

    payload = {
        "header":"DKU  일반채용정보",

        "title1":title[0],
        "description1":description[0],
        "url1":href[0],

        "title2": title[1],
        "description2": description[1],
        "url2": href[1],

        "title3": title[2],
        "description3": description[2],
        "url3": href[2],

        "title4": title[3],
        "description4": description[3],
        "url4": href[3],

        "title5": title[4],
        "description5": description[4],
        "url5": href[4],

        "button1":"홈페이지 바로가기"
    }
    data = {"template_args": json.dumps(payload), "template_id": 18310}


    result = requests.post(url, headers=header, data=data)
    if result.ok == True:
        print("log - kakao_send_to_me log > OK")
    else:
        print("log - kakao_send_to_me log > FAIL")
        print(result)

if __name__ == '__main__':
    print(">")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 1. refresh access_token, refresh_token
    refresh_token = ""
    with open("./data/token.txt", "r") as fr:
        refresh_token = fr.readline();
        print("current token is  >> ", refresh_token)

    new_token = getAccessToken(refresh_token)
    access_token = new_token['access_token']
    refresh_token = ""
    try:
        refresh_token = new_token['refresh_token']
        with open("./data/token.txt", "w") as fw:
            fw.write(refresh_token)
    except Exception as e:
        pass

    # 2. send to kakao-msg.
    file_path = "./data/posts.csv"
    result = pd.read_csv(file_path)

    numbers = result["Number"].tolist()
    campuses = result["Campus"].tolist()
    areas = result["Area"].tolist()
    companys= result["Company"].tolist()
    titles = result["Title"].tolist()
    hrefs = result["Href"].tolist()
    statuss= result["Status"].tolist()
    r_dates= result["R_date"].tolist()
    d_dates= result["D_date"].tolist()

    fr = open("./data/known_posts.txt", "r", encoding='utf-8')
    known_posts = fr.readlines()
    fr.close()

    total_number = len(titles)
    fw = open("./data/known_posts.txt", "a", encoding='utf-8')

    print(">" * 60 + "start sending kakaotalk message ...")
    number = []; campuse = []; area = []; company = []; title = []; href = []; status = []; r_date = []; d_date = []
    cnt = 0
    for each in range(total_number):
        post = titles[each]
        if post+"\n" not in known_posts:
            cnt = cnt + 1
            fw.write(post+"\n")
            number.append(numbers[each])
            campuse.append(campuses[each])
            area.append(areas[each])
            company.append(companys[each])
            title.append(titles[each])
            href.append(hrefs[each])
            status.append(statuss[each])
            r_date.append(r_dates[each])
            d_date.append(d_dates[each])

            if cnt%5==0:
                kakao_send_to_me(number, campuse, area, company, title, href, status, r_date, d_date, KAKAO_TOKEN=access_token)
                number = []; campuse = []; area = []; company = []; title = []; href = []; status = []; r_date = []; d_date = []

    if cnt % 5 != 0:
        enum = cnt % 5
        for idx in range(enum,5):
            number.append(None); campuse.append(None); area.append(None); company.append(None); title.append(None); href.append(None); status.append(None); r_date.append(None); d_date.append(None)

        kakao_send_to_me(number, campuse, area, company, title, href, status, r_date, d_date, KAKAO_TOKEN=access_token)
        number = []; campuse = [];area = []; company = []; title = []; href = []; status = []; r_date = []; d_date = []

    fw.close()
    print(">" * 60 + "finish sending kakaotalk message ...")