import codecs
import re
import requests
import lxml
import urllib
import urllib.parse
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
f = codecs.open('C:/Users/CrosstreetB/results.json', 'w', encoding="utf-8")
f2 = codecs.open('C:/Users/CrosstreetB/station_name.txt', 'r')
tup_station = f2.read().splitlines()
tup_menu = ('파스타', '치킨', '한식', '삼겹살', '초밥', '회', '중국', '곱창')

for stn_item in tup_station:
    key_stn = stn_item
    key_stn += '역 '

    for menu_item in tup_menu:
        key_menu = menu_item
        key_menu += ' '
        keyword = '맛집'
        key = key_stn + key_menu + keyword
        key_en = urllib.parse.quote(key.encode('utf8'))
        
        headers = {
            'user-agent' : str(ua.random)
        }
        url = 'https://search.naver.com/search.naver?where=post&query=' + key_en + '&st=sim&sm=tab_opt&date_from=20140101&date_to=20141231&date_option=8&srchby=all&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom20140101to20141231'
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, "lxml")
        # output : '1-10 / 8,778건' 형태
        output = soup.find('span', {'class' :'title_num'})
        if output is None:
            continue
        output = output.text

        # Regex 사용, Output으로부터 건 수 추출
        p = re.compile('[\s][\d]*[,]*[\d]+')
        s = p.search(output)

        if s != None:
            # [,] 삭제
            post_num = int(s.group().replace(',', ''))
            f.write('{' + '\"' + 'station_name' + '\"' + ':' + '\"' + key_stn + '\",' +
                '\"' + 'food_name' + '\"' + ':' + '\"' + key_menu + '\",'
                '\"' + 'post_num' + '\"' + ':' + '\"' + str(post_num) + '\"}' + '\n')
        else:
            pass
    #time.sleep(10)

f.close()
f2.close()