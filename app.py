import streamlit as st

from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.parse import * 
from bs4 import BeautifulSoup 
import json 
import pandas as pd
from dateutil.parser import parse
from datetime import date, timedelta
import time
from selenium.webdriver.common.by import By
import time
import urllib.request

st.set_page_config(page_title="종목뉴스")

today = time.strftime("%Y-%m-%d")

def naver_api_news(search_text):
    news = []
    client_id = "G0iATjx0bSkbzmjo37Jo"
    client_secret = 'pLJzj9sJz6'
    searchTxt = urllib.parse.quote(search_text)
    url = 'https://openapi.naver.com/v1/search/news.json?query='+searchTxt+'&display='+str(100)+'&sort=sim'
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    response_body_str = response.read().decode('utf-8')
    temp1 = json.loads(response_body_str)
    for i in temp1['items']:
        aa1 = i['title']
        title = BeautifulSoup(aa1,'html.parser').text
        link = i['link']
        description = i['description']
        pubDate = i['pubDate']
        news.append([title,link,pubDate, description])
    return news

def date_convert(x):
    x= parse(x)
    return x


def news_df_convert(news):
    df_news = pd.DataFrame(news, columns=['제목','주소','발행일','설명'])
    df_news= df_news.drop_duplicates(['제목','주소','발행일'])
    df_news['발행일3'] = pd.to_datetime(df_news['발행일'])
    df_news['발행일2'] = df_news['발행일'].apply(date_convert).dt.date
    df_news_today = df_news.sort_values('발행일3',ascending=False).copy()
    df_news_today = df_news_today.reset_index()
    return df_news_today

## 업로드테스트


if __name__ == "__main__":
    with st.sidebar:
            search_term = st.text_input("뉴스검색어를 입력해주세요")
    
    if search_term:
        st.write("")
        search_text = search_term
        news = naver_api_news(search_text)
        news_df = news_df_convert(news)
        news_all = []
        for idx, row in news_df.iterrows():
            title = row['제목']
            date1 = row['발행일']
            link = row['주소']
            des = row['설명']
            soup = BeautifulSoup(des,'html.parser')
            des = soup.get_text()
            st.write(date1)
            st.write(title)
            st.write(des)
            st.write(link)

