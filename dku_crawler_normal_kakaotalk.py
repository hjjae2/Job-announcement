import requests
import json
import pandas as pd
import datetime

def renewToken(refreshToken):
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=refresh_token&client_id=@client_id&refresh_token=" + refreshToken
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    reponse = requests.request("POST", url, data=payload, headers=headers)
    new_token = json.loads(reponse.text)

    # Renew refresh_token.
    refresh_token = ""
    try:
        refresh_token = new_token['refresh_token']
        with open("./data/token.txt", "w") as fw:
            fw.write(refresh_token)
    except Exception as e:
        pass

    return new_token

def getAccessToken(renewToken):
    refresh_token = ""
    with open("./data/token.txt", "r") as fr:
        refresh_token = fr.readline();
        print("current token is  >> ", refresh_token)

    new_token = renewToken(refresh_token)
    access_token = new_token['access_token']

    return access_token

def getCrawledPosts(_file_path):
    file_path = _file_path
    result = pd.read_csv(file_path)

    numbers = result["Number"].tolist()
    campuses = result["Campus"].tolist()
    areas = result["Area"].tolist()
    companys = result["Company"].tolist()
    titles = result["Title"].tolist()
    hrefs = result["Href"].tolist()
    statuss = result["Status"].tolist()
    r_dates = result["R_date"].tolist()
    d_dates = result["D_date"].tolist()

    posts = list()
    posts.append(numbers)
    posts.append(campuses)
    posts.append(areas)
    posts.append(companys)
    posts.append(titles)
    posts.append(hrefs)
    posts.append(statuss)
    posts.append(r_dates)
    posts.append(d_dates)
    return posts

def getKnownPosts(_file_path):
    fr = open(_file_path, "r", encoding='utf-8')
    known_posts = fr.readlines()
    fr.close()

    return known_posts

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

def sendKakao(posts, known_posts, access_token, kakao_send_to_me):
    # Posts is a list[numbers, campuses, areas, companys, titles, hrefs, statuss, r_dates, d_dates].
    numbers = posts[0]
    campuses = posts[1]
    areas = posts[2]
    companys = posts[3]
    titles = posts[4]
    hrefs = posts[5]
    statuss = posts[6]
    r_dates = posts[7]
    d_dates = posts[8];

    # Newly sent posts are written to known_file
    known_file_path = "./data/known_normal_posts.txt"
    fw = open(known_file_path, "a", encoding='utf-8')

    print(">" * 60 + "start sending kakaotalk message ...")
    number = []; campuse = []; area = []; company = []; title = []; href = []; status = [];  r_date = []; d_date = []

    cnt = 0
    total_number = len(titles)
    for each in range(total_number):
        post = titles[each]
        if post + "\n" not in known_posts:
            cnt = cnt + 1
            fw.write(post + "\n")
            number.append(numbers[each])
            campuse.append(campuses[each])
            area.append(areas[each])
            company.append(companys[each])
            title.append(titles[each])
            href.append(hrefs[each])
            status.append(statuss[each])
            r_date.append(r_dates[each])
            d_date.append(d_dates[each])

            if cnt % 5 == 0:
                kakao_send_to_me(number, campuse, area, company, title, href, status, r_date, d_date, KAKAO_TOKEN=access_token)
                number = []; campuse = []; area = []; company = []; title = []; href = []; status = []; r_date = []; d_date = []

    if cnt % 5 != 0:
        enum = cnt % 5
        for idx in range(enum, 5):
            number.append(None);
            campuse.append(None);
            area.append(None);
            company.append(None);
            title.append(None);
            href.append(None);
            status.append(None);
            r_date.append(None);
            d_date.append(None)

        kakao_send_to_me(number, campuse, area, company, title, href, status, r_date, d_date, KAKAO_TOKEN=access_token)
        number = []; campuse = []; area = []; company = []; title = []; href = []; status = []; r_date = []; d_date = []

    fw.close()
    print(">" * 60 + "finish sending kakaotalk message ...")

if __name__ == '__main__':
    print(">")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 1. Renew refresh_token, get access_token.
    access_token = getAccessToken(renewToken)

    # 2. Read crawled posts.
    file_path = "./data/normal_posts.csv"
    posts = getCrawledPosts(file_path)

    # 3. Read known posts. This means already posted data.
    known_file_path = "./data/known_normal_posts.txt"
    known_posts = getKnownPosts(known_file_path)

    # 4. send to kakao-msg.
    file_path = "./data/normal_posts.csv"
    known_file_path = "./data/known_normal_posts.txt"
    sendKakao(posts, known_posts, access_token, kakao_send_to_me)