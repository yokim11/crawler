
# coding: utf-8

# In[196]:



from time import sleep
import requests
import json
from pytz import timezone
from datetime import datetime
#from urllib.parse import urlencode
from bs4 import BeautifulSoup
#import urllib3
#urllib3.disable_warnings()


# In[197]:

def send_teamroom(data):
    #test방-> url = 'https://teamroom.nate.com/api/webhook/5e5e40b3/d2DptYOG1nL1sXHlRCONSPLq'
    url = 'https://teamroom.nate.com/api/webhook/5e5e40b3/U0oZQ6zqS5RRc4cnJabacNNf'
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
    
    query = {'content': data}

    ret = requests.post(url, data=query, headers=headers, verify=False)
    


# In[198]:

def craw_nate():
    req = requests.get('https://javastwo.nate.com/nate/getlivekeyword?callback=RSKS.Init', verify=False)
    total_data1 = req.text
    total_data2 = total_data1.replace('var arrHotRecent=\'', '')
    total_data3 = total_data2.replace('\';RSKS.Init();', '')

    nate_index = 0
    nate_rankings = list()
    for r in json.loads(total_data3):
        #print (r)
        nate_index = nate_index + 1
        nate_rankings.insert(nate_index, r[1])
        #print (r['rank'], r['keyword'])

    return (nate_rankings)


# In[199]:

def craw_naver():
    ## Naver 실시간 검색어
    req = requests.get('https://www.naver.com/srchrank?frm=main&ag=all&gr=1&ma=-2&si=0&en=0&sp=0', verify=False)
    var = json.loads(req.text)
    naver_list = var['data']

    naver_ranking_time = var['ts']
    naver_index = 0
    naver_rankings = list()
    for r in naver_list:
        if (naver_index >= 10):
            break
        naver_index = naver_index + 1
        naver_rankings.insert(r['rank'], r['keyword'])
        #print (r['rank'], r['keyword'])
        
    return (naver_rankings)


# In[200]:

def craw_kakao():
    ## KAKAO 실시간 검색어
    base_url = 'https://m.daum.net'
    req = requests.get(base_url, verify=False)
    soup = BeautifulSoup(req.text, "html.parser")
    total_data = soup.find(attrs={'class': 'keyissue_area'})
    total_data2 = total_data.find_all(attrs={'class': 'txt_issue'})

    kakao_index = 0
    kakao_rankings = list()
    for d in total_data2:
        kakao_index = kakao_index + 1
        kakao_rankings.insert(kakao_index, d.text)
        #print(kakao_index, d.text)
        
    return (kakao_rankings)


# In[201]:

def craw_zum():
    ## ZUM 실시간 검색어
    base_url = 'http://www.zum.com'
    req = requests.get(base_url, verify=False)
    soup = BeautifulSoup(req.text, "html.parser")
    total_data = soup.find(attrs={'class': 'rank_list d_rank_list d_rank_keyword_0'})
    total_data2 = total_data.find_all(attrs={'class': 'keyword d_keyword'})
    
    before_keyword = 'a'
    zum_index = 0
    zum_rankings = list()
    for d in total_data2:
        if (d.text == before_keyword):
            before_keyword = d.text
            continue
        zum_index = zum_index + 1
        zum_rankings.insert(zum_index, d.text)
        before_keyword = d.text
        #print(d.text)
        
    return (zum_rankings)


# In[202]:

def create_message(title, data_rankings):
    content = list()
    content.append('● {:_<30} \n'.format(title))
    for i in range(10):
        content.append('[{:2d}] {}\n'.format(i+1, data_rankings[i]))

    return (''.join(content))


# In[ ]:

if __name__ == "__main__":
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    while (True):
        KST = datetime.now(timezone('Asia/Seoul'))

        content = []
        content.append('● 크롤링 : {}\n'.format(KST))
        content.append(create_message('NATE', craw_nate()))
        content.append(create_message('NAVER', craw_naver()))
        content.append(create_message('KAKAO', craw_kakao()))
        content.append(create_message('ZUM', craw_zum()))

        send_teamroom(''.join(content))

        sleep(5*60)
