# main.py
import streamlit as st  
from news_crawler import make_url, articles_crawler, get_news_content  
from translator import translate_news  
from ai_quiz_generator import generate_quiz  
from utils import clean_text  

st.title('AI 영어 지문 및 문제 생성기') 

# 사용자로부터 검색 키워드 입력 받기
search = st.text_input("검색할 키워드를 입력해주세요")
start_page, end_page = 1, 2  # 크롤링할 시작 및 종료 페이지 설정

if search:  # 검색 키워드가 입력된 경우
    urls = make_url(search, start_page, end_page)  # 키워드로 크롤링할 URL 목록 생성
    news_urls = [url for page in urls for url in articles_crawler(page)]  # 각 페이지의 뉴스 기사 링크 추출
    news_df = get_news_content(news_urls)  # 뉴스 기사 제목, 내용, 날짜 크롤링하여 데이터프레임 생성
    
    news_contents = [clean_text(content) for content in news_df['content']]  # 기사 내용 정리(클린업) 수행
    translated_news = translate_news(news_contents)  # 정리된 기사 내용 영어로 번역

    # 각 뉴스 기사에 대해 제목을 버튼으로 표시하고, 클릭 시 내용 및 퀴즈 생성
    for date, title, content in zip(news_df['date'], news_df['title'], translated_news):
        if st.button(title):  # 기사 제목을 버튼으로 표시
            st.write(f"날짜: {date}")  # 기사 날짜 표시
            st.write(content)  # 번역된 기사 내용 표시
            
            quiz = generate_quiz(content)  # 기사 내용을 기반으로 퀴즈 생성
            st.write("생성된 퀴즈:")  # 생성된 퀴즈 설명 텍스트 표시
            st.write(quiz)  # 생성된 퀴즈 출력
