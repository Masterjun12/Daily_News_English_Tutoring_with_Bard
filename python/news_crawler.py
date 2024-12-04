# news_crawler.py
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd
from config import HEADERS  

# 페이지 번호 계산 함수 (네이버 뉴스의 경우 페이지별 번호 규칙이 다름)
def make_pg_num(num):
    return num + 9 * (num - 1) if num > 1 else num

# 크롤링할 URL 목록을 생성하는 함수 (검색어, 시작 페이지, 종료 페이지)
def make_url(search, start_pg, end_pg):
    urls = [
        f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search}&start={make_pg_num(i)}"
        for i in range(start_pg, end_pg + 1)
    ]
    return urls  # 생성된 URL 리스트 반환

# HTML을 가져와 뉴스 기사 링크들을 추출하는 함수
def articles_crawler(url):
    response = requests.get(url, headers=HEADERS)  # 요청 보내기
    html = BeautifulSoup(response.text, "html.parser")  # HTML 파싱
    articles = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")  # 뉴스 기사 링크 요소 선택
    return [a.attrs['href'] for a in articles if 'news.naver.com' in a.attrs['href']]  # 네이버 뉴스 링크만 필터링하여 반환

# 뉴스 기사 링크들로부터 제목, 내용, 날짜 정보를 가져오는 함수
def get_news_content(news_urls):
    titles, contents, dates = [], [], []  # 제목, 내용, 날짜를 저장할 리스트 생성
    for url in tqdm(news_urls):  # 진행 상황 표시를 위한 tqdm 사용
        response = requests.get(url, headers=HEADERS)  # 각 뉴스 기사에 대해 요청 보내기
        html = BeautifulSoup(response.text, "html.parser")  # HTML 파싱

        # 제목 추출 (각 페이지별 구조가 다를 수 있어서 조건문 사용)
        title = html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2") or \
                html.select_one("#content > div.end_ct > div > h2")
        title = re.sub('<[^>]*>', '', str(title))  # HTML 태그 제거

        # 내용 추출 (다른 구조에 따라 선택)
        content = html.select("div#dic_area") or html.select("#articeBody")
        content_text = re.sub('<[^>]*>', '', ''.join(map(str, content)))  # HTML 태그 제거 후 텍스트로 변환

        # 날짜 추출 (각 페이지별 구조 차이를 고려)
        date = html.select_one("div.media_end_head_info_datestamp span") or \
               html.select_one("#content > div.end_ct > div > div.article_info > span > em")
        date = re.sub('<[^>]*>', '', str(date))  # HTML 태그 제거

        titles.append(title)  # 제목 리스트에 추가
        contents.append(content_text)  # 내용 리스트에 추가
        dates.append(date)  # 날짜 리스트에 추가

    # DataFrame 생성 후 중복 제거하여 반환
    return pd.DataFrame({'date': dates, 'title': titles, 'content': contents, 'link': news_urls}).drop_duplicates()
