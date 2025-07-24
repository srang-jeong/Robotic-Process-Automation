import streamlit as st
import pandas as pd
import feedparser
from urllib.parse import quote
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from wordcloud import WordCloud
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import os
import requests
import newspaper
from newspaper import Article
import nltk
from fpdf import FPDF

nltk.download('punkt')

# 모델 및 라이브러리 초기화
@st.cache_resource
def load_models():
    summarizer = SentenceTransformer("jhgan/ko-sroberta-multitask")
    sentiment_ko = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_en = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    okt = Okt()
    return summarizer, sentiment_ko, sentiment_en, okt

summarizer, sentiment_ko, sentiment_en, okt = load_models()

# 기본 UI 설정
st.set_page_config(page_title="📰 AI/로봇 뉴스 대시보드", layout="wide")
st.title("🧠🛠️🕹️ AI/로봇 뉴스 요약 대시보드")
st.caption("뉴스 본문 크롤링")

# 필터 및 옵션
KEYWORDS = ["AI", "로봇", "로봇감정", "로봇성격", "IT", "산업데이터", "데이터시스템"]
selected_keywords = st.sidebar.multiselect("🔍 관심 키워드", KEYWORDS, default=KEYWORDS)
extra_kw = st.sidebar.text_input("➕ 추가 키워드 (쉼표구분)")
if extra_kw:
    selected_keywords += [kw.strip() for kw in extra_kw.split(",") if kw.strip()]
lang_option = st.sidebar.radio("🌍 뉴스 언어", ["한국어", "영어"])
max_items = st.sidebar.slider("📰 키워드별 최대 뉴스 수", 1, 15, 5)
start_date = st.sidebar.date_input("📅 시작일", None)
end_date = st.sidebar.date_input("📅 종료일", None)
view_type = st.sidebar.radio("뉴스 보기 방식", ["카드뷰", "테이블"])
show_network = st.sidebar.checkbox("📊 키워드-감성 네트워크 그래프", False)
show_memo = st.sidebar.checkbox("📝 북마크 메모쓰기 활성화", True)

if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []
if "memo" not in st.session_state:
    st.session_state["memo"] = dict()

# 텍스트 정리 함수
def clean_text(html):
    return BeautifulSoup(html, "html.parser").get_text(separator=" ").strip()

# 뉴스 본문 크롤링 & 텍스트 추출
@st.cache_data(show_spinner=True)
def get_article_text(url):
    try:
        article = Article(url, language='ko' if lang_option == "한국어" else 'en')
        article.download()
        article.parse()
        article.nlp()
        return article.text
    except Exception:
        return ""

# AI 요약 함수
def summarize(text, num_sent=3):
    if not text or len(text) < 10:
        return ""
    sentences = text.replace("!", ".").split(". ")
    if len(sentences) <= num_sent:
        return text
    emb = summarizer.encode(sentences)
    center = emb.mean(axis=0)
    scores = [util.pytorch_cos_sim([center], [e])[0][0] for e in emb]
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sent]
    return ". ".join([sentences[i] for i in sorted(top_idx)])

# 키워드 추출
def extract_keywords(text, n=5):
    nouns = [w for w in okt.nouns(text) if len(w) > 1]
    freq = pd.Series(nouns).value_counts() if nouns else pd.Series([])
    return ", ".join(freq[:n].index) if not freq.empty else ""

# 감성 분석
def get_sentiment(text, lang="ko"):
    try:
        if lang == "ko":
            result = sentiment_ko(text[:256])
            return result[0]["label"]
        else:
            result = sentiment_en(text)
            return {"POSITIVE": "긍정", "NEGATIVE": "부정"}.get(result[0]["label"], "중립")
    except:
        return "중립"

# 뉴스 RSS에서 제목 등 기본 수집 + 본문 별도 크롤링
@st.cache_data(show_spinner=True)
def fetch_news(keyword, lang="ko"):
    q = quote(keyword)
    rss_url = f"https://news.google.com/rss/search?q={q}&hl={'ko' if lang=='ko' else 'en'}&gl=KR&ceid=KR:{'ko' if lang=='ko' else 'en'}"
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:max_items]:
        try:
            title = entry.title
            link = entry.link
            date = entry.get("published", datetime.now().strftime("%Y-%m-%d"))
            raw_summary = entry.summary if hasattr(entry, "summary") else title
            summary = clean_text(raw_summary)

            # 본문 크롤링 추가
            article_text = get_article_text(link)
            if article_text:
                summary = article_text  # 본문 우선 사용

            # 요약, 키워드, 감성
            summ = summarize(summary, num_sent=3)
            kws = extract_keywords(summary)
            senti = get_sentiment(summary, lang=lang)

            articles.append({
                "키워드": keyword, "제목": title, "링크": link, "날짜": date,
                "본문": summary, "요약": summ, "키워드추출": kws, "감성": senti
            })
        except Exception as e:
            continue
    return pd.DataFrame(articles)

# 전체 뉴스 수집 및 필터링
df_list = [fetch_news(k, lang="ko" if lang_option=="한국어" else "en") for k in selected_keywords]
news_df = pd.concat(df_list).drop_duplicates(subset=["링크"])
news_df["날짜"] = pd.to_datetime(news_df["날짜"], errors="coerce")

if start_date:
    news_df = news_df[news_df["날짜"] >= pd.to_datetime(start_date)]
if end_date:
    news_df = news_df[news_df["날짜"] <= pd.to_datetime(end_date)]

# 감성 이모지 매핑
senti_emoji = {"긍정": "🟢", "부정": "🔴", "중립": "🟡"}
news_df["감성이모지"] = news_df["감성"].map(senti_emoji)

st.markdown(f"### 총 뉴스 건수: {len(news_df)}건")
if news_df.empty:
    st.warning("조건에 맞는 뉴스가 없습니다.")
    st.stop()

# 시계열, 감성 분포, 키워드 빈도
with st.expander("🧮 뉴스 통계 및 트렌드", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("키워드별 뉴스 건수")
        st.bar_chart(news_df["키워드"].value_counts())
    with col2:
        st.subheader("👍👎 감성 분포")
        fig = px.pie(news_df, names="감성", title="감성 분포")
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.subheader("🔥 인기 키워드 Top10")
        all_kws = ", ".join(news_df["키워드추출"].dropna())
        kws = [k.strip() for k in all_kws.split(",") if k.strip()]
        kw_freq = pd.Series(kws).value_counts().head(10)
        st.bar_chart(kw_freq)

    emo_daily = news_df.groupby([news_df["날짜"].dt.date, "감성"]).size().unstack().fillna(0)
    st.subheader("📆 일별 감성 시계열")
    st.line_chart(emo_daily)

# 키워드별 감성 비교
with st.expander("🆚 키워드별 감성 비교"):
    selected = st.multiselect("비교할 키워드 선택", news_df["키워드"].unique())
    if selected:
        df_comp = news_df[news_df["키워드"].isin(selected)]
        fig = px.histogram(df_comp, x="감성", color="키워드", barmode="group", title="키워드별 감성 비교")
        st.plotly_chart(fig)

# 뉴스 목록 출력 및 북마크 + 메모
st.markdown("## 뉴스 목록")
for idx, row in news_df.iterrows():
    key = f"bm_{hash(row['링크'])}"
    with st.container():
        st.markdown(f"### [{row['제목']}]({row['링크']})")
        st.caption(f"📅 {row['날짜'].date()}")
        st.markdown(f"🧾 {row['요약']}")
        st.markdown(f"감성: {senti_emoji.get(row['감성'], '🟡')} {row['감성']}")
        st.markdown(f"`{row['키워드추출']}`")
        if row['감성'] == "부정":
            st.warning("🚨 부정적 뉴스입니다.")
        if st.button("⭐ 북마크", key=key):
            if row["링크"] not in st.session_state["bookmarks"]:
                st.session_state["bookmarks"].append(row["링크"])
        if show_memo:
            memo_key = f"memo_{key}"
            memo_text = st.text_area("메모", st.session_state.get(memo_key, ""),
                                    key=memo_key, height=60)

# 북마크한 뉴스 PDF 저장
with st.expander("📥 북마크 모아보기 & PDF 저장"):
    bm_df = news_df[news_df["링크"].isin(st.session_state["bookmarks"])]
    if len(bm_df):
        for _, row in bm_df.iterrows():
            st.markdown(f"- [{row['제목']}]({row['링크']})")
        if st.button("북마크 뉴스 PDF 저장"):
            pdf = FPDF()
            pdf.add_page()

            # 한글 유니코드 지원 폰트 파일 경로 (확장자 .ttf가 빠졌으면 추가하세요)
            font_path = r"C:\Users\EDU03-17\Downloads\Noto_Sans_KR\static\NotoSansKR-Regular.ttf"

            # 유니코드(TTF) 폰트 등록
            pdf.add_font('NotoSansKR', '', font_path, uni=True)
            pdf.set_font('NotoSansKR', '', 12)

            pdf.cell(200, 10, "북마크 뉴스 요약", 0, 1, 'C')

            for _, row in bm_df.iterrows():
                key = f"bm_{hash(row['링크'])}"
                memo_key = f"memo_{key}"
                memo = st.session_state.get(memo_key, "")

                entry = (
                    "📰 제목 : " + row['제목'] + "\n"
                    + "🧾 요약 : " + row['요약'] + "\n"
                    + "🏷️ 키워드 : " + row['키워드추출'] + "\n"
                    + "❤️ 감성 : " + row['감성'] + " " + senti_emoji.get(row['감성'], "") + "\n"
                    + (f"📝 메모 : {memo}\n" if memo else "")
                    + "🔗 링크 : " + row['링크'] + "\n"
                    + "-"*50 + "\n"
                )
                pdf.multi_cell(0, 10, entry)

            temp = BytesIO()
            pdf.output(temp)
            st.download_button("⬇️ PDF 다운로드", data=temp.getvalue(), file_name="북마크_뉴스.pdf")
    else:
        st.info("📌 북마크된 뉴스가 없습니다. 뉴스 옆 버튼으로 북마크하세요.")